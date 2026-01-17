<template>
    <div
        class="flex flex-col md:flex-row md:bg-primary-light md:shadow md:border-neutral-100 md:rounded-xl md:p-5 md:py-2"
    >
        <div
            class="w-full md:w-auto bg-green-500 md:bg-transparent p-3 rounded-t-xl hidden md:flex items-center"
        >
            <h2
                class="text-xl font-semibold text-white md:text-green-700 text-center"
            >
                Mood log
            </h2>
        </div>
        <article
            class="flex flex-col md:flex-row md:content-center grow items-center border rounded-xl md:rounded-t-none p-5 md:p-0 bg-primary-light border-neutral-100 border-t border-t-transparent shadow md:shadow-none md:border-none"
        >
            <div class="md:h-full flex flex-col justify-end w-full">
                <section
                    class="grid grid-cols-7 gap-1 md:gap-7 w-full md:w-auto md:flex items-center justify-center"
                >
                    <div
                        v-for="(log, index) in moodLogs"
                        :key="index"
                        class="flex flex-col items-center p-1 rounded-xl"
                    >
                        <span class="font-sans text-2xl md:text-xl">{{
                            moodEmojis[log.mood]
                        }}</span>
                        <p class="text-xs mt-2 md:mt-1 text-text font-medium">
                            {{ log.day }}
                        </p>
                    </div>
                </section>
            </div>

            <Button
                class="text-white mt-2 md:mt-0 w-full md:w-auto md:ml-auto"
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
