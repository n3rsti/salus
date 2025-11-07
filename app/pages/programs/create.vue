<template>
    <div>
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between"
        >
            <h1 class="text-green-700 text-xl font-semibold">Create program</h1>
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
                        placeholder="Describe your program..."
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
import type { Program } from "~/models/program.model";

const name = ref("");
const description = ref("");

const config = useRuntimeConfig();

async function submitForm() {
    const program: Program = {
        name: name.value,
        description: description.value,
        duration_days: 1,
        image_url: "",
        language: "pl",
    };

    await $fetch(`${config.public.apiBase}/api/programs`, {
        method: "POST",
        body: program,
        onResponse: async (response) => {
            if (response.response.status == 200) {
                const data: Program = response.response._data;
                await navigateTo(`/programs/${data.id}`);
            }
        },
    });
}
</script>
