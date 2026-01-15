<template>
    <div
        class="flex flex-col lg:flex-row lg:bg-primary-light lg:shadow lg:border-neutral-100 lg:rounded-xl lg:p-4 lg:py-2"
    >
        <div
            class="w-full lg:w-auto bg-green-500 lg:bg-transparent p-3 lg:p-0 rounded-t-xl hidden lg:flex items-center"
        >
            <h2
                class="text-xl font-semibold text-white lg:text-green-700 text-center"
            >
                Mood log
            </h2>
        </div>
        <article
            class="flex flex-col lg:flex-row lg:content-center grow items-center border rounded-xl lg:rounded-t-none p-5 lg:p-0 bg-primary-light border-neutral-100 border-t border-t-transparent shadow lg:shadow-none lg:border-none"
        >
            <div class="lg:h-full flex flex-col justify-end w-full">
                <section
                    class="grid grid-cols-7 gap-1 lg:gap-7 w-full lg:w-auto lg:flex items-center justify-center"
                >
                    <div
                        v-for="(log, index) in moodLogs"
                        :key="index"
                        class="flex flex-col items-center p-1 rounded-xl"
                    >
                        <span class="font-sans text-2xl lg:text-xl">{{
                            moodEmojis[log.mood]
                        }}</span>
                        <p class="text-xs mt-2 lg:mt-1 text-text font-medium">
                            {{ log.day }}
                        </p>
                    </div>
                </section>
            </div>

            <Button
                class="text-white mt-2 lg:mt-0 w-full lg:w-auto lg:ml-auto"
                variant="success"
            >
                Add daily log
            </Button>
        </article>
    </div>
</template>
<script setup lang="ts">
import { faker } from "@faker-js/faker";
import { Button } from "./ui/button";

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
