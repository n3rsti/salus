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
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3"
        >
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

const { data: activities } = await useFetch<Activity[]>(
    "http://localhost:8080/api/activities",
    {
        server: true,
    },
);

faker.seed(1);

const name = faker.person.firstName();

const programs: Program[] = [];

for (let i = 0; i < 3; i++) {
    const newProgram: Program = {
        language: "en",
        id: 0,
        name: faker.commerce.product(),
        description: faker.commerce.productDescription(),
        duration_minutes: faker.number.int({ min: 1, max: 10 }),
        rating: faker.number.float({ min: 0.1, max: 5.0, fractionDigits: 1 }),
        image: faker.image.url({ width: 400, height: 300 }),
    };

    if (faker.number.int({ min: 0, max: 1 }) == 1) {
        newProgram.progress = faker.number.int({ min: 0, max: 100 });
    }
    programs.push(newProgram);
}
</script>
