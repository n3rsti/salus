<template>
    <AppSearch
        :activities="activities"
        :programs="programs"
        :not-found="notFound"
        :is-loading="isLoading"
        @fetch="fetchSearchResults"
        @clear="clearData"
    >
    </AppSearch>
</template>

<script setup lang="ts">
import type { Activity } from "~/models/activity.model";
import type { Program } from "~/models/program.model";

const { $api } = useNuxtApp();

const programs = ref<Program[]>([]);
const activities = ref<Activity[]>([]);
const notFound = ref(false);
const isLoading = ref(false);

async function fetchSearchResults(input: string, controller: AbortController) {
    notFound.value = false;
    isLoading.value = true;
    try {
        const [a, p] = await Promise.all([
            $api<Activity[]>(
                `/api/activities/?search=${encodeURIComponent(input)}&limit=3`,
                { signal: controller.signal },
            ),
            $api<Program[]>(
                `/api/programs/?search=${encodeURIComponent(input)}&limit=3`,
                { signal: controller.signal },
            ),
        ]);

        activities.value = a;
        programs.value = p;

        if (a.length + p.length == 0) notFound.value = true;
    } catch (err: any) {
        if (err?.name !== "AbortError") console.error(err);
    } finally {
        isLoading.value = false;
    }
}

function clearData() {
    programs.value = [];
    activities.value = [];
}
</script>
