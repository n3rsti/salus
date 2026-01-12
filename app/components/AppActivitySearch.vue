<template>
    <AppSearch
        :not-found="notFound"
        :is-loading="isLoading"
        :reset-key="resetKey"
        @fetch="fetchSearchResults"
        @clear="clearData"
    >
        <template #not-found>
            Unfortunately no activity was found based on your search.
        </template>
        <template #loading>
            <div class="flex flex-col rounded-md py-2 px-2 gap-2">
                <div class="flex items-center gap-2">
                    <Skeleton class="h-8 aspect-square rounded-lg" />
                    <Skeleton class="w-20 h-4 rounded-md" />
                    <Skeleton class="w-12 h-5 rounded-md" />
                    <Skeleton class="ml-auto w-20 h-5 rounded-md" />
                </div>
                <Skeleton class="w-full h-5 rounded-md" />
            </div>
        </template>
        <template #default>
            <div class="text-center py-2">
                <h2 class="font-semibold">Search here...</h2>
                <p class="text-sm">Search for activity.</p>
            </div>
        </template>
        <template v-if="activities.length > 0" #results>
            <h2 v-if="activities.length > 0" class="text-sm font-semibold">
                Activities
            </h2>
            <button
                v-for="activity in activities"
                :key="activity.id"
                type="button"
                class="py-2 px-2 rounded-md border flex flex-col gap-2 hover:bg-accent transition-colors shadow-xs"
                @click.prevent.stop="addActivity(activity)"
            >
                <div class="flex items-center gap-2">
                    <img
                        :src="'/media/' + activity.image_url"
                        alt=""
                        class="h-8 aspect-square rounded-lg"
                    />
                    <h3
                        class="font-semibold text-sm hover:underline cursor-pointer"
                    >
                        {{ activity.name }}
                    </h3>
                    <Badge
                        class="text-xs rounded-md"
                        :class="DifficultiesColors[activity.difficulty]"
                        >{{ Difficulties[activity.difficulty] }}</Badge
                    >
                    <span class="flex items-center ml-auto text-xs gap-1">
                        <Icon name="ic:outline-access-time" />
                        {{ activity.duration_minutes }} minutes
                    </span>
                </div>
                <p class="text-sm text-accent-content text-start">
                    {{ activity.description }}
                </p>
            </button>
        </template>
    </AppSearch>
</template>

<script setup lang="ts">
import { Difficulties, DifficultiesColors } from "~/constants/difficulty";
import type { Activity } from "~/models/activity.model";

import { Badge } from "./ui/badge";
import { Skeleton } from "./ui/skeleton";

const props = defineProps<{
    day: number;
}>();

const emit = defineEmits<{
    addActivity: [activity: Activity, day: number];
}>();

const { $api } = useNuxtApp();

const activities = ref<Activity[]>([]);
const notFound = ref(false);
const isLoading = ref(false);

const resetKey = ref(0);

const searchStore = useSearchStore();

function addActivity(activity: Activity) {
    emit("addActivity", activity, props.day);
    close();
}

function close() {
    searchStore.close();
    resetKey.value++;
}

async function fetchSearchResults(input: string, controller: AbortController) {
    notFound.value = false;
    isLoading.value = true;
    try {
        const [a] = await Promise.all([
            $api<Activity[]>(
                `/api/activities/?search=${encodeURIComponent(input)}`,
                { signal: controller.signal },
            ),
        ]);

        activities.value = a;

        if (a.length == 0) notFound.value = true;
    } catch (err: any) {
        if (err?.name !== "AbortError") console.error(err);
    } finally {
        isLoading.value = false;
    }
}

function clearData() {
    activities.value = [];
}
</script>
