<template>
    <div>
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between"
        >
            <h1 class="text-green-700 text-xl font-semibold">Programs</h1>
            <NuxtLink to="/programs/create">
                <AppButton :color="'green'">Create</AppButton>
            </NuxtLink>
        </div>

        <AppProgramCard
            v-for="program in programs"
            :key="program.id"
            :program="program"
        />
    </div>
</template>

<script setup lang="ts">
import type { Program } from "~/models/program.model";

const config = useRuntimeConfig();

const { data: programs } = await useFetch<Program[]>(
    `${config.public.apiBase}/api/programs`,
);
</script>
