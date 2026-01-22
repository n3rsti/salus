<template>
    <div class="w-full grid grid-cols-1 md:grid-cols-2 gap-3">
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between shadow-sm col-span-2"
        >
            <h1 class="text-green-700 text-xl font-semibold">Mood log</h1>

            <NuxtLink :to="todayLog ? '/mood/edit' : '/mood/add'">
                <Button variant="success">
                    {{ todayLog ? "Edit today's mood" : "Add current mood" }}
                </Button>
            </NuxtLink>
        </div>

        <div v-for="section in dateSections" :key="section.key">
            <div class="text-sm font-semibold text-primary mb-2">
                {{ section.label }}
            </div>

            <div class="flex flex-col gap-3">
                <div
                    v-for="log in section.items"
                    :key="log.id"
                    class="p-4 rounded-xl bg-card border border-primary-dark shadow-sm"
                >
                    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 text-sm">
                        <p>
                            😊 Mood: <strong>{{ log.mood }}</strong>
                        </p>
                        <p>
                            😴 Sleep: <strong>{{ log.sleep_score }}</strong>
                        </p>
                        <p>
                            😣 Stress: <strong>{{ log.stress }}</strong>
                        </p>
                        <p>
                            🎯 Focus: <strong>{{ log.focus }}</strong>
                        </p>
                        <p>
                            🏃 Activity:
                            <strong>{{ log.physical_activity }}</strong>
                        </p>
                        <p>
                            🍷 Alcohol:
                            <strong>{{ log.alcohol_intake }}</strong>
                        </p>
                    </div>

                    <p
                        v-if="log.notes"
                        class="mt-3 text-xs text-muted-foreground italic"
                    >
                        "{{ log.notes }}"
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { Button } from "~/components/ui/button";
onMounted(() => {
    refresh();
});
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
const { data, refresh } = await useFetch<DailyLog[]>("/api/daily-logs", {
    method: "GET",
    credentials: "include",
    $fetch: $api,
});

const logs = computed(() =>
    [...(data.value ?? [])].sort(
        (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
    ),
);

const formatDate = (date: string) =>
    new Date(date).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
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
                label: formatDate(log.date),
                items: [log],
            });
        } else {
            last.items.push(log);
        }
    }

    return sections;
});
</script>
