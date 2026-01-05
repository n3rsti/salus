<template>
    <AppActivityForm
        :activity="emptyActivity"
        @update="submitForm"
    ></AppActivityForm>
</template>

<script setup lang="ts">
import type { Activity } from "~/models/activity.model";

const { $api } = useNuxtApp();

const emptyActivity: Activity = {
    name: "",
    description: "",
    duration_minutes: 0,
    image_url: "",
    difficulty: 1,
};

async function submitForm(activity: Activity, file: File) {
    const formData = new FormData();
    formData.append("activity_in", JSON.stringify(activity));

    formData.append("image", file);
    await $api(`/api/activities`, {
        method: "POST",
        body: formData,
        onResponse: async (response) => {
            if (response.response.status == 200) {
                const data: Activity = response.response._data;
                await navigateTo(`/activities/${data.id}`);
            }
        },
    });
}
</script>
