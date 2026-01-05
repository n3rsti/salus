<template>
    <AppProgramForm
        :initial-data="program"
        @submit="submitForm"
        @delete="deleteProgram"
    ></AppProgramForm>
</template>

<script setup lang="ts">
import type { Program } from "~/models/program.model";

const route = useRoute();

const { data: program } = await useFetch<Program>(
    `/api/programs/${route.params.id}`,
);

if (!program.value) {
    throw createError({
        statusCode: 404,
        statusMessage: "Program Not Found",
    });
}

const { $api } = useNuxtApp();

async function submitForm(program: Program, file: File | undefined) {
    const formData = new FormData();
    formData.append("program_update", JSON.stringify(program));

    if (file) formData.append("image", file);

    await $api(`/api/programs/${route.params.id}`, {
        method: "PUT",
        body: formData,
        onResponse: async (response) => {
            if (response.response.status == 200) {
                const data: Program = response.response._data;
                await navigateTo(`/programs/${data.id}`);
            }
        },
    });
}

async function deleteProgram() {
    try {
        await $api(`/api/programs/${route.params.id}`, {
            method: "DELETE",
        });
        await navigateTo("/programs");
    } catch (error) {
        console.error("Failed to delete program:", error);
    }
}
</script>
