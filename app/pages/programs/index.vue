<template>
    <div class="flex flex-col items-center">
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between shadow-sm w-full"
        >
            <h1 class="text-green-700 text-xl font-semibold">Programs</h1>
            <NuxtLink to="/programs/create">
                <Button variant="success">Create</Button>
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

        <Button
            v-if="programs && programs.length > 0"
            class="mt-4"
            variant="success"
            @click="fetchMorePrograms(10)"
        >
            Load more
        </Button>
    </div>
</template>

<script setup lang="ts">
import { Button } from "~/components/ui/button";
import type { Program } from "~/models/program.model";

const { data: programs } = await useFetch<Program[]>(`/api/programs?limit=20`);

async function fetchMorePrograms(limit: number) {
    const current = programs.value ?? [];
    if (current.length === 0) return;

    const { data, error } = await useFetch<Program[]>(
        `/api/programs?skip=${current.length}&limit=${limit}`,
    );

    if (error.value) return;

    const more = data.value ?? [];
    if (more.length === 0) return;

    programs.value = [...current, ...more];
}
</script>
