<template>
    <div>
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between"
        >
            <h1 class="text-green-700 text-xl font-semibold">Activities</h1>
            <NuxtLink to="/activities/create">
                <AppButton :color="'green'">Create</AppButton>
            </NuxtLink>
        </div>

        <AppACtivityCard
            v-for="activity in activities"
            :key="activity.id"
            :activity="activity"
        />
    </div>
</template>

<script setup lang="ts">
import type { Activity } from "~/models/activity.model";

const { data: activities } = await useFetch<Activity[]>(
    "http://localhost:8080/api/activities",
);
</script>
