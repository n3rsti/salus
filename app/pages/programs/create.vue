<template>
    <AppProgramForm @submit="submitForm"></AppProgramForm>
</template>

<script setup lang="ts">
import type { Program } from "~/models/program.model";

const { $api } = useNuxtApp();

async function submitForm(program: Program, file: File | undefined) {
    const formData = new FormData();
    formData.append("program_in", JSON.stringify(program));

    if (file) formData.append("image", file);

    await $api(`/api/programs`, {
        method: "POST",
        body: formData,
        onResponse: async (response) => {
            if (response.response.status == 200) {
                const data: Program = response.response._data;
                await navigateTo(`/programs/${data.id}`);
            }
        },
    });
}
</script>
