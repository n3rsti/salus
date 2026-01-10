<template>
    <div>
        <h2 class="font-semibold text-xl mb-4 flex">Programs</h2>
        <section
            v-if="programs && programs.length > 0"
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3"
        >
            <AppProgramCard
                v-for="program in programs"
                :key="program.id"
                :program="program"
            />
        </section>
        <section v-else>
            <h3>Not found</h3>
        </section>
        <h2 class="font-semibold text-xl mt-10 mb-4 flex">Activities</h2>
        <section
            v-if="activities && activities.length > 0"
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3"
        >
            <AppActivityCard
                v-for="activity in activities"
                :key="activity.id"
                :activity="activity"
            />
        </section>
        <section v-else>
            <h3 class="text-center py-10">Not found</h3>
        </section>
    </div>
</template>
<script setup lang="ts">
import type { Activity } from "~/models/activity.model";
import type { Program } from "~/models/program.model";

const route = useRoute();

const queryParams = route.query;
const search = queryParams.search;

const { data: activities } = await useFetch<Activity[]>(
    search ? `/api/activities?search=${search}` : `/api/activities`,
);

const { data: programs } = await useFetch<Program[]>(
    search ? `/api/programs?search=${search}` : `/api/programs`,
);
</script>
