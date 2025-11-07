<template>
    <div class="flex flex-col">
        <div class="w-full bg-green-500 p-3 rounded-t-xl hidden lg:block">
            <h2 class="text-xl font-semibold text-white text-center">
                Mood log
            </h2>
        </div>
        <article
            class="flex flex-col grow items-center border rounded-xl lg:rounded-t-none p-5 bg-primary-light border-neutral-100 border-t border-t-transparent shadow"
        >
            <div class="lg:h-1/2 flex flex-col justify-end w-full">
                <section class="grid grid-cols-7 gap-1 w-full">
                    <div
                        v-for="(log, index) in moodLogs"
                        :key="index"
                        class="flex flex-col items-center p-1 rounded-xl"
                    >
                        <span class="font-sans text-2xl lg:text-4xl">{{
                            moodEmojis[log.mood]
                        }}</span>
                        <p class="text-xs mt-2 text-text">{{ log.day }}</p>
                    </div>
                </section>
            </div>

            <AppButton
                class="text-white mt-2 w-full lg:mt-auto"
                :color="'green'"
            >
                Add daily log
            </AppButton>
        </article>
    </div>
</template>
<script setup lang="ts">
import { faker } from "@faker-js/faker";

interface MoodLog {
    mood: number;
    day: string;
}

const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const moodEmojis = ["💀", "😕", "😐", "🤠", "🥳"];
const moodLogs: MoodLog[] = [];

days.forEach((day) => {
    moodLogs.push({
        mood: faker.number.int({ min: 0, max: 4 }),
        day: day,
    });
});
</script>
