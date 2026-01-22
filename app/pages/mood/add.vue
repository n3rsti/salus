<template>
    <div class="min-w-1/2 mx-auto p-6 bg-card border rounded-xl shadow-sm">
        <h1 class="text-xl font-semibold text-primary mb-6">
            Add today's mood
        </h1>

        <form class="flex flex-col gap-5" @submit.prevent="submitForm">
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
                    class="textarea textarea-bordered w-full"
                    placeholder="Optional notes..."
                />
            </div>

            <Button
                type="submit"
                variant="success"
                class="self-end"
                :disabled="loading"
            >
                Save mood
            </Button>
        </form>
    </div>
</template>

<script setup lang="ts">
import { Button } from "~/components/ui/button";
import { Input } from "~/components/ui/input";
const { $api } = useNuxtApp();

const today = () => {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(
        2,
        "0",
    )}-${String(d.getDate()).padStart(2, "0")}`;
};

const loading = ref(false);

const form = reactive({
    date: today(),
    mood: 5,
    sleep_score: 5,
    stress: 5,
    focus: 5,
    physical_activity: 5,
    alcohol_intake: 10,
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

async function submitForm() {
    loading.value = true;

    try {
        await $api("/api/daily-logs", {
            method: "POST",
            body: { ...form },
        });

        await navigateTo("/mood-log");
    } finally {
        loading.value = false;
    }
}
</script>
