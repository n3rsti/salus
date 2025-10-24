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
            <AppCard
                v-for="activity in activities"
                :key="activity.id"
                :image="activity.image"
                :title="activity.name"
                :description="activity.description"
            >
                <div class="flex items-center justify-between mt-auto">
                    <p class="text-muted/90 text-sm flex items-center gap-1">
                        <Icon name="ic:outline-access-time" />
                        {{ activity.duration }}
                        minutes
                    </p>
                    <p class="text-sm flex items-center text-text gap-1">
                        {{ activity.rating }}/5
                        <Icon
                            name="material-symbols:star-rounded"
                            class="text-yellow-400 text-2xl"
                        />
                    </p>
                </div>
                <AppButton
                    class="w-full shadow-sm border-t-transparent text-white mt-3"
                    :color="'green_dark'"
                >
                    View info
                    <Icon class="text-lg ml-2" name="ic:round-remove-red-eye" />
                </AppButton>
            </AppCard>
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
        duration: faker.number.int({ min: 1, max: 10 }),
        rating: faker.number.float({ min: 0.1, max: 5.0, fractionDigits: 1 }),
        image: faker.image.url({ width: 400, height: 300 }),
    };

    if (faker.number.int({ min: 0, max: 1 }) == 1) {
        newProgram.progress = faker.number.int({ min: 0, max: 100 });
    }
    programs.push(newProgram);
}
</script>
