<template>
    <div>
        <div class="p-4 rounded-xl bg-primary-light mb-4">
            <h2 class="text-green-700 text-xl">
                Good evening,
                <span class="text-green-800 font-semibold">{{ name }}</span
                >! 👋
            </h2>
        </div>
        <section
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3"
        >
            <AppMoodCard class="lg:col-span-2"></AppMoodCard>

            <AppProgramCard
                v-for="program in programs"
                :key="program.id"
                :program="program"
            />
            <AppActivityCard
                v-for="activity in activities"
                :key="activity.id"
                :activity="activity"
            />
        </section>
    </div>
</template>
<script setup lang="ts">
import type { Activity } from "~/models/activity.model";
import { faker } from "@faker-js/faker";
import type { Program } from "~/models/program.model";

const { data: activities } = await useFetch<Activity[]>(`/api/activities`);

const { data: programs } = await useFetch<Program[]>(`/api/programs`);

faker.seed(1);

const name = faker.person.firstName();
</script>
