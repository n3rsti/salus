<template>
    <div>
        <div class="p-4 rounded-xl bg-primary-light mb-4">
            <h2 class="text-green-700 text-xl">
                Good evening,
                <span class="font-medium text-green-800">{{ name }}</span
                >! 👋
            </h2>
        </div>
        <section class="grid grid-cols-1 gap-2">
            <AppCard
                v-for="activity in activities"
                :key="activity.id"
                :model-value="activity"
            />
        </section>
    </div>
</template>
<script setup lang="ts">
import type { Activity } from "~/models/activity.model";
import { ActivityBuilder } from "~/models/activity.model";
import { faker } from "@faker-js/faker";

const name = faker.person.firstName();

const activities: Activity[] = [];

for (let i = 0; i < 10; i++) {
    activities.push(
        new ActivityBuilder()
            .setName(faker.commerce.product())
            .setDescription(faker.commerce.productDescription())
            .setDuration(faker.number.int({ max: 10 }))
            .setRating(
                faker.number.float({ min: 0.1, max: 5.0, fractionDigits: 1 }),
            )
            .setImage(faker.image.url({ width: 400, height: 300 }))
            .build(),
    );
}
</script>
