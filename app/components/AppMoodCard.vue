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
                        <p
                            class="text-xs mt-2 md:mt-1 text-primary font-medium"
                        >
                            {{ log.day }}
                        </p>
                    </div>
                </section>
            </div>

            <NuxtLink :to="todayLog ? '/mood/edit' : '/mood/add'">
                <Button variant="success">
                    {{ todayLog ? "Edit today's mood" : "Add current mood" }}
                </Button>
            </NuxtLink>
        </article>
    </div>
</template>
<script setup lang="ts">
import { faker } from "@faker-js/faker";
import { Button } from "./ui/button";
const { $api } = useNuxtApp();

interface DailyLog {
    id: number;
    date: string;
    mood: number;
    sleep_score: number;
    stress: number;
    focus: number;
    physical_activity: number;
    alcohol_intake: number;
    notes: string;
}
const todayKey = () => {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(
        2,
        "0",
    )}-${String(d.getDate()).padStart(2, "0")}`;
};
const todayLog = computed(() =>
    logs.value.find((log) => log.date.slice(0, 10) === todayKey()),
);
const { data } = await useFetch<DailyLog[]>("/api/daily-logs", {
    method: "GET",
    credentials: "include",
    $fetch: $api,
});

const logs = computed(() =>
    [...(data.value ?? [])].sort(
        (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
    ),
);

//----------------------//
faker.seed(1234);
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
