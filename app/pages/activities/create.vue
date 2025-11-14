<template>
    <div>
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">
                Create activity
            </h1>
        </div>

        <div class="mb-4">
            <form
                action=""
                class="grid grid-cols-1 md:grid-cols-2 gap-2 max-md:bg-primary-light rounded-xl max-md:shadow-sm"
                @submit.prevent="submitForm"
            >
                <div
                    class="flex flex-col gap-4 rounded-xl bg-primary-light md:shadow-sm p-4"
                >
                    <div class="flex flex-col gap-2">
                        <AppFormLabel for="name">Name</AppFormLabel>
                        <AppFormInput
                            id="name"
                            v-model="name"
                            type="text"
                            placeholder="Enter name"
                            required
                        />
                    </div>
                    <div class="flex flex-col gap-2 flex-1 min-h-0">
                        <AppFormLabel for="description"
                            >Description</AppFormLabel
                        >

                        <AppFormTextArea
                            id="description"
                            v-model="description"
                            class="md:flex-1 md:min-h-0"
                            name="description"
                            placeholder="Describe your activity..."
                            required
                        />
                    </div>
                </div>
                <div
                    class="flex flex-col gap-4 rounded-xl bg-primary-light md:shadow-sm p-4"
                >
                    <div class="flex flex-col gap-2">
                        <AppFormLabel for="duration"
                            >Duration
                            <span class="text-muted/70 text-xs"
                                >(minutes)</span
                            ></AppFormLabel
                        >
                        <AppFormInput
                            id="duration"
                            v-model="duration"
                            type="number"
                            min="0"
                            required
                        />
                    </div>
                    <div class="flex flex-col gap-2">
                        <AppFormLabel for="image"
                            >Image
                            <span class="text-muted/70 text-xs"
                                >(url)</span
                            ></AppFormLabel
                        >
                        <AppFormInput
                            id="image"
                            v-model="image"
                            type="text"
                            placeholder="https://example.com"
                            required
                        />
                    </div>
                    <div class="flex flex-col gap-2">
                        <AppFormLabel>Difficulty</AppFormLabel>

                        <label
                            v-for="difficulty in difficulties"
                            :key="difficulty.name"
                            :for="difficulty.name.toLowerCase()"
                            class="cursor-pointer"
                            :class="difficulty.classes.text"
                        >
                            <AppRadioButton
                                class="border"
                                :class="
                                    selectedDifficulty == difficulty.value
                                        ? difficulty.classes.border
                                        : 'border-primary-dark font-light'
                                "
                            >
                                <input
                                    :id="difficulty.name.toLowerCase()"
                                    v-model="selectedDifficulty"
                                    type="radio"
                                    name="difficulty"
                                    :value="difficulty.value"
                                    class="radio bg-white"
                                    :class="difficulty.classes.radio"
                                />
                                <p class="ml-3">
                                    {{ difficulty.name }}
                                </p>
                            </AppRadioButton>
                        </label>
                    </div>
                </div>
                <AppButton
                    type="submit"
                    :color="'green'"
                    class="w-full md:col-span-2"
                    >Create</AppButton
                >
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Activity } from "~/models/activity.model";

const name = ref("");
const description = ref("");
const selectedDifficulty = ref(1);
const duration = ref(0);
const image = ref("");

interface Difficulty {
    name: string;
    value: number;
    classes: Record<string, string>;
}

const difficulties: Difficulty[] = [
    {
        name: "Easy",
        value: 1,
        classes: {
            radio: "radio-success",
            text: "text-success",
            border: "border-success",
        },
    },
    {
        name: "Moderate",
        value: 2,
        classes: {
            radio: "radio-info",
            text: "text-info",
            border: "border-info",
        },
    },
    {
        name: "Hard",
        value: 3,
        classes: {
            radio: "radio-error",
            text: "text-error",
            border: "border-error",
        },
    },
];

const config = useRuntimeConfig();

async function submitForm() {
    const activity: Activity = {
        name: name.value,
        description: description.value,
        duration_minutes: duration.value,
        image_url: image.value,
        difficulty: selectedDifficulty.value,
    };

    await $fetch(`${config.public.apiBase}/api/activities`, {
        method: "POST",
        body: activity,
        onResponse: async (response) => {
            if (response.response.status == 200) {
                const data: Activity = response.response._data;
                await navigateTo(`/activities/${data.id}`);
            }
        },
    });
}
</script>
