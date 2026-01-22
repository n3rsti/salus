<template>
    <div class="min-w-1/2 mx-auto p-6 bg-card border rounded-xl shadow-sm">
        <h1 class="text-xl font-semibold text-primary mb-6">
            Edit today's mood
        </h1>

        <form
            v-if="loaded"
            class="flex flex-col gap-5"
            @submit.prevent="submitForm"
        >
            <div
                v-for="field in fields"
                :key="field.key"
                class="flex flex-col gap-1"
            >
                <label class="text-sm font-medium">
                    {{ field.label }}
                </label>

                <Input
                    type="number"
                    min="0"
                    max="10"
                    v-model.number="form[field.key]"
                    required
                />
            </div>

            <div class="flex flex-col gap-1">
                <label class="text-sm font-medium">Notes</label>
                <Input
                    v-model="form.notes"
                    class="textarea textarea-bordered w-full min-h-[100px]"
                />
            </div>

            <Button
                type="submit"
                variant="success"
                class="self-end"
                :disabled="loading"
            >
                Save changes
            </Button>
        </form>

        <p v-else class="text-sm text-muted-foreground">Loading mood data...</p>
    </div>
</template>
<script setup lang="ts">
import { Button } from "~/components/ui/button";
import { Input } from "~/components/ui/input";
import { navigateTo } from "#app";

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

const loading = ref(false);
const loaded = ref(false);
const logId = ref<number | null>(null);

const form = reactive({
    mood: 0,
    sleep_score: 0,
    stress: 0,
    focus: 0,
    physical_activity: 0,
    alcohol_intake: 0,
    notes: "",
});

const fields = [
    { key: "mood", label: "Mood" },
    { key: "sleep_score", label: "Sleep quality" },
    { key: "stress", label: "Stress level" },
    { key: "focus", label: "Focus" },
    { key: "physical_activity", label: "Physical activity" },
    { key: "alcohol_intake", label: "Alcohol intake" },
] as const;
const { data } = await useFetch<DailyLog[]>("/api/daily-logs", {
    method: "GET",
    credentials: "include",
    $fetch: $api,
    cache: "no-store",
});

const todayLog = computed(() =>
    data.value?.find((log) => log.date.slice(0, 10) === todayKey()),
);

if (todayLog.value) {
    const log = todayLog.value;
    logId.value = log.id;

    form.mood = log.mood;
    form.sleep_score = log.sleep_score;
    form.stress = log.stress;
    form.focus = log.focus;
    form.physical_activity = log.physical_activity;
    form.alcohol_intake = log.alcohol_intake;
    form.notes = log.notes ?? "";

    loaded.value = true;
} else {
    await navigateTo("/mood/add");
}
async function submitForm() {
    if (!logId.value) return;

    loading.value = true;

    try {
        const payload = {
            mood: form.mood,
            sleep_score: form.sleep_score,
            stress: form.stress,
            focus: form.focus,
            physical_activity: form.physical_activity,
            alcohol_intake: form.alcohol_intake,
            notes: form.notes,
        };

        await $api(`/api/daily-logs/${logId.value}`, {
            method: "PUT",
            body: payload,
        });

        await navigateTo("/mood-log");
    } finally {
        loading.value = false;
    }
}
</script>
