<template>
    <div
        v-if="requiresSurvey"
        class="fixed inset-0 z-50 flex items-center justify-center"
    >
        <div class="absolute inset-0 bg-black/60"></div>
        <div class="relative bg-white rounded-xl p-6 w-full max-w-lg space-y-4">
            <h2 class="text-green-700 text-xl">
                Hello,
                <span class="text-green-800 font-semibold">{{
                    store.username
                }}</span
                >! 👋
            </h2>
            <h3 class="text-xl font-semibold">Personal Preferences Survey</h3>

            <p class="text-sm text-gray-600">
                Please indicate how important it is for you to improve the
                following areas.
            </p>

            <div v-for="field in fields" :key="field.key">
                <label class="text-sm font-medium">
                    {{ field.label }}
                </label>
                <input
                    type="range"
                    min="1"
                    max="10"
                    v-model.number="form[field.key]"
                    class="w-full accent-green-500"
                />
                <div class="text-xs text-gray-500">
                    Value: {{ form[field.key] }}
                </div>
            </div>

            <Button
                class="w-full bg-green-600 text-white py-2 rounded"
                @click="submit"
            >
                Save preferences
            </Button>
        </div>
    </div>
</template>

<script setup lang="ts">
const requiresSurvey = useState<boolean>("requiresSurvey");

const form = reactive({
    mood: 5,
    sleep: 5,
    stress: 5,
    focus: 5,
    physical_activity: 5,
});

const fields = [
    { key: "mood", label: "Mood improvement" },
    { key: "sleep", label: "Sleep quality" },
    { key: "stress", label: "Stress reduction" },
    { key: "focus", label: "Focus and concentration" },
    { key: "physical_activity", label: "Physical activity" },
];
const store = useUserStore();
const submit = async () => {
    await $fetch("/api/user-preferences", {
        method: "POST",
        body: form,
        credentials: "include",
    });
    requiresSurvey.value = false;
};
</script>
