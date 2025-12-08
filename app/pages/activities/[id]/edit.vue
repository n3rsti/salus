<template>
    <AppActivityForm
        :activity="activity || emptyActivity"
        @update="updateActivity"
        @delete="deleteActivity"
    ></AppActivityForm>
</template>

<script setup lang="ts">
import type { Activity } from "~/models/activity.model";

const route = useRoute();

const { data: activity } = await useFetch<Activity>(
    `/api/activities/${route.params.id}`,
);

if (!activity.value) {
    throw createError({
        statusCode: 404,
        statusMessage: "Activity Not Found",
    });
}

const emptyActivity: Activity = {
    name: "",
    description: "",
    duration_minutes: 0,
    image_url: "",
    difficulty: 1,
};

async function deleteActivity() {
    await $fetch(`/api/activities/${activity.value?.id}`, {
        method: "DELETE",
        onResponse: async (response) => {
            if (response.response.status == 200) {
                await navigateTo(`/activities/`);
            }
        },
    });
}

async function updateActivity(activity: Activity) {
    await $fetch(`/api/activities/`, {
        method: "PUT",
        body: activity,
        onResponse: async (response) => {
            if (response.response.status == 200) {
                const data: Activity = response.response._data;
                await navigateTo(`/activities/${data.id}`);
            }
        },
    });
}
</script>
