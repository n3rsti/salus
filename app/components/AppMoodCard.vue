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
                        v-for="section in lastSections"
                        :key="section.key"
                        class="flex flex-col items-center p-1 rounded-xl"
                    >
                        <span class="text-2xl md:text-xl">
                            {{ getEmoji(section.items[0]) }}
                        </span>
                        <p
                            class="text-xs mt-2 md:mt-1 text-primary font-medium"
                        >
                            {{ formatDateShort(section.items[0].date) }}
                        </p>
                    </div>
                </section>
            </div>

            <NuxtLink :to="todayLog ? '/mood/edit' : '/mood/add'">
                <Button variant="success" class="ml-4 md:ml-8">
                    {{ todayLog ? "Edit today's mood" : "Add current mood" }}
                </Button>
            </NuxtLink>
        </article>
    </div>
</template>

<script setup lang="ts">
import { Button } from "~/components/ui/button";
import { onMounted, computed, ref } from "vue";

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

const formatDateShort = (date: string) => {
    const d = new Date(date);
    return `${d.getDate()} ${d.toLocaleString("en-US", { month: "short" })}`;
};
const { data, refresh } = await useFetch<DailyLog[]>("/api/daily-logs", {
    method: "GET",
    credentials: "include",
    $fetch: $api,
    cache: "no-store",
});

const logs = computed(() => {
    const allLogs = data.value ?? [];
    allLogs.sort(
        (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
    );
    return allLogs.slice(0, 7).reverse();
});
function dateKey(date: string) {
    const d = new Date(date);
    return `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;
}

const dateSections = computed(() => {
    const sections: { key: string; label: string; items: DailyLog[] }[] = [];

    for (const log of logs.value) {
        const key = dateKey(log.date);
        const last = sections.at(-1);

        if (!last || last.key !== key) {
            sections.push({
                key,
                label: formatDateShort(log.date),
                items: [log],
            });
        } else {
            last.items.push(log);
        }
    }

    return sections;
});
const lastSections = computed(() => dateSections.value.slice(-7));
const todayLog = computed(() =>
    (data.value ?? []).find((log) => log.date.slice(0, 10) === todayKey()),
);
function getEmoji(log: DailyLog) {
    const scores = [
        { key: "mood", value: log.mood, emoji: "😊" },
        { key: "sleep_score", value: log.sleep_score, emoji: "😴" },
        { key: "stress", value: log.stress, emoji: "😣" },
        { key: "focus", value: log.focus, emoji: "🎯" },
        { key: "physical_activity", value: log.physical_activity, emoji: "🏃" },
        { key: "alcohol_intake", value: log.alcohol_intake, emoji: "🍷" },
    ];

    const maxScore = Math.max(...scores.map((s) => s.value));
    const best = scores.find((s) => s.value === maxScore);
    return best?.emoji ?? "❔";
}
</script>
