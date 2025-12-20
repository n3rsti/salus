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

async function submitForm(program: Program) {
    try {
        const data = await $api<Program>(`/api/programs/${route.params.id}`, {
            method: "PUT",
            body: program,
        });

        if (data?.id) {
            await navigateTo(`/programs/${data.id}`);
        }
    } catch (error) {
        console.error("Failed to create program:", error);
    }
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
