<template>
    <div>
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">Activities</h1>
            <NuxtLink to="/activities/create">
                <AppButton :color="'green'">Create</AppButton>
            </NuxtLink>
        </div>

        <section
            class="w-full grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3"
        >
            <AppActivityCard
                v-for="activity in activities"
                :key="activity.id"
                :activity="activity"
            />
        </section>
    </div>
</template>

<script setup lang="ts">
import type { Activity } from "~/models/activity.model";

const config = useRuntimeConfig();

const { data: activities } = await useFetch<Activity[]>(
    `${config.public.apiBase}/api/activities`,
);
</script>
