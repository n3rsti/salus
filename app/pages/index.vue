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
            <AppCard
                v-for="program in programs"
                :key="program.id"
                :data="program"
            />
            <AppCard
                v-for="activity in activities"
                :key="activity.id"
                :data="activity"
            />
        </section>
    </div>
</template>
<script setup lang="ts">
import type { Activity } from "~/models/activity.model";
import { ActivityBuilder } from "~/models/activity.model";
import { faker } from "@faker-js/faker";
import { ProgramBuilder, type Program } from "~/models/program.model";

const name = faker.person.firstName();

const programs: Program[] = [];
const activities: Activity[] = [];

for (let i = 0; i < 3; i++) {
    const newProgram = new ProgramBuilder()
        .setName(faker.commerce.product())
        .setDescription(faker.commerce.productDescription())
        .setDuration(faker.number.int({ min: 1, max: 10 }))
        .setRating(
            faker.number.float({ min: 0.1, max: 5.0, fractionDigits: 1 }),
        )
        .setImage(faker.image.url({ width: 400, height: 300 }));

    if (faker.number.int({ min: 0, max: 1 }) == 1) {
        newProgram.setProgress(faker.number.int({ min: 0, max: 100 }));
    }
    programs.push(newProgram.build());
}

for (let i = 0; i < 10; i++) {
    activities.push(
        new ActivityBuilder()
            .setName(faker.commerce.product())
            .setDescription(faker.commerce.productDescription())
            .setDuration(faker.number.int({ min: 1, max: 10 }))
            .setRating(
                faker.number.float({ min: 0.1, max: 5.0, fractionDigits: 1 }),
            )
            .setImage(faker.image.url({ width: 400, height: 300 }))
            .build(),
    );
}
</script>
