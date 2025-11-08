<template>
    <div>
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between"
        >
            <h1 class="text-green-700 text-xl font-semibold">
                Create activity
            </h1>
        </div>

        <div class="p-4 rounded-xl bg-primary-light mb-4">
            <form
                action=""
                class="flex flex-col gap-4"
                @submit.prevent="submitForm"
            >
                <div class="flex flex-col gap-2">
                    <AppFormLabel for="name">Name</AppFormLabel>
                    <AppFormInput
                        id="name"
                        v-model="name"
                        type="text"
                        placeholder="Enter name"
                        required
                    />
                </div>
                <div class="flex flex-col gap-2">
                    <AppFormLabel for="description">Description</AppFormLabel>
                    <AppFormTextArea
                        v-model="description"
                        placeholder="Describe your activity..."
                        required
                    ></AppFormTextArea>
                </div>
                <AppButton type="submit" :color="'green'" class="w-full"
                    >Create</AppButton
                >
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Activity } from "~/models/activity.model";

const name = ref("");
const description = ref("");

const config = useRuntimeConfig();

async function submitForm() {
    const activity: Activity = {
        name: name.value,
        description: description.value,
        duration_minutes: 15,
        image_url: "",
        difficulty: 1,
    };

    await $fetch(`${config.public.apiBase}/api/activities`, {
        method: "POST",
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
