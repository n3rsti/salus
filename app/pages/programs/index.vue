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

        <section
            class="w-full grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3"
        >
            <AppProgramCard
                v-for="program in programs"
                :key="program.id"
                :program="program"
            />
        </section>
    </div>
</template>

<script setup lang="ts">
import type { Program } from "~/models/program.model";

const config = useRuntimeConfig();

const { data: programs } = await useFetch<Program[]>(
    `${config.public.apiBase}/api/programs`,
);
</script>
