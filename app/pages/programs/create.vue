<template>
    <div>
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">Create program</h1>
        </div>

        <div class="rounded-xl mb-4">
            <form
                action=""
                class="grid grid-cols-1 md:grid-cols-2 gap-4"
                @submit.prevent="submitForm"
            >
                <div
                    class="flex flex-col gap-4 bg-primary-light p-4 rounded-xl shadow-sm"
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
                    <div class="flex flex-col gap-2">
                        <AppFormLabel for="description"
                            >Description</AppFormLabel
                        >
                        <AppFormTextArea
                            id="description"
                            v-model="description"
                            name="description"
                            placeholder="Describe your program..."
                            required
                        ></AppFormTextArea>
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
                </div>
                <div
                    class="flex flex-col gap-2 bg-primary-light shadow-sm p-4 rounded-xl"
                >
                    <div
                        v-for="day in days"
                        :key="day.num"
                        class="rounded-xl border-primary-dark border collapse collapse-arrow shadow-inner"
                    >
                        <input type="checkbox" checked />
                        <div class="collapse-title font-semibold text-text">
                            Day {{ day.num }}
                        </div>
                        <div class="px-4 collapse-content flex flex-col gap-2">
                            <div class="flex flex-col gap-2">
                                <AppFormLabel :for="day.num + '-description'"
                                    >Description</AppFormLabel
                                >
                                <AppFormTextArea
                                    :id="day.num + '-description'"
                                    v-model="day.description"
                                    class="focus:border-text"
                                    placeholder="Describe the day..."
                                    required
                                ></AppFormTextArea>
                            </div>

                            <div>
                                <AppFormLabel :for="day.num + '-activities'"
                                    >Add activities</AppFormLabel
                                >
                                <div class="flex gap-2">
                                    <AppFormInput
                                        :id="day.num + '-activities'"
                                        v-model="day.input"
                                        type="number"
                                        min="1"
                                        placeholder="Enter activity id"
                                        class="focus:border-text"
                                    />
                                    <AppButton
                                        class="w-1/4 rounded-lg bg-text text-xs"
                                        :color="'black'"
                                        type="button"
                                        @click="addActivity(day.input, day.num)"
                                        >Add</AppButton
                                    >
                                </div>
                            </div>
                            <div
                                v-for="activity in day.activities"
                                :key="activity.id"
                                class="flex flex-col w-full gap-2 p-3 border border-primary-dark rounded-xl mt-2"
                            >
                                <div class="flex items-center w-full">
                                    <img
                                        :src="activity.image_url"
                                        alt=""
                                        class="h-8 aspect-square rounded-lg"
                                    />
                                    <p
                                        class="text-text font-medium text-sm ml-2"
                                    >
                                        {{ activity.name }}
                                    </p>
                                    <AppButton
                                        :color="'red'"
                                        class="ml-auto btn-xs text-xs"
                                        @click="
                                            removeActivity(activity.id, day.num)
                                        "
                                        >Remove</AppButton
                                    >
                                </div>
                                <div class="w-full">
                                    <p class="text-muted/80 text-xs">
                                        {{ activity.description }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <AppButton
                        class="text-xs"
                        :color="'black'"
                        type="button"
                        @click="addDay"
                        >Add day</AppButton
                    >
                </div>

                <AppButton
                    type="submit"
                    :color="'green'"
                    class="w-full mt-3 md:col-span-2"
                    >Create</AppButton
                >
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Activity } from "~/models/activity.model";
import type { Program } from "~/models/program.model";
import type { ProgramDay } from "~/models/program_day.model";

const name = ref("");
const description = ref("");
const image = ref("");

interface Day {
    num: number;
    input: Ref<number | undefined>;
    activities: Array<Activity>;
    description: string;
}

const days = ref<Day[]>([
    {
        num: 1,
        input: ref<number | undefined>(undefined),
        activities: [],
        description: "",
    },
]);

function removeActivity(activity_id: number | undefined, day: number) {
    if (activity_id == undefined) return;
    const dayObj = days.value[day - 1];

    if (dayObj && dayObj.activities) {
        dayObj.activities = dayObj?.activities.filter(
            (a) => a.id != activity_id,
        );
    }
}

async function addActivity(activity_id: number | undefined, day: number) {
    if (activity_id == undefined) return;

    const dayObj = days.value[day - 1];
    const isAlreadyAdded =
        dayObj?.activities.find((a) => a.id == activity_id) != undefined;

    if (isAlreadyAdded) {
        dayObj.input = undefined;
        return;
    }

    await $fetch(`/api/activities/${activity_id}/`, {
        method: "GET",
        onResponse: async (response) => {
            if (response.response.status === 200) {
                const data: Activity = response.response._data;

                if (dayObj) {
                    dayObj.activities.push(data);

                    dayObj.input = undefined;
                }
            }
        },
    });
}

function addDay() {
    const newDay: Day = {
        num: days.value.length + 1,
        input: ref<number | undefined>(undefined),
        activities: [],
        description: "",
    };

    days.value.push(newDay);
}

const config = useRuntimeConfig();

async function createDays(program_id: number) {
    for (const day of days.value) {
        const newDay: ProgramDay = {
            description: day.description,
            day_number: day.num - 1,
            program_id,
        };

        await createDay(newDay);
    }
}

async function createDay(day: ProgramDay) {
    await $fetch(`/api/programs/days`, {
        method: "POST",
        body: day,
        onResponse: async (response) => {
            if (response.response.status == 200) {
                const data: ProgramDay = response.response._data;
                if (data.id) {
                    await linkDays(day, data.id);
                }
            }
        },
    });
}

async function linkDays(day: ProgramDay, program_day_id: number) {
    const dayObj = days.value[day.day_number];
    for (const activity of dayObj?.activities || []) {
        if (activity.id) {
            await linkActivity(program_day_id, activity.id);
        }
    }
}

async function linkActivity(program_day_id: number, activity_id: number) {
    await $fetch(
        `/api/programs/days/${program_day_id}/activities/${activity_id}/`,
        {
            method: "POST",
        },
    );
}

async function submitForm() {
    const program: Program = {
        name: name.value,
        description: description.value,
        duration_days: days.value.length,
        image_url: image.value,
        language: "pl",
    };

    await $fetch(`/api/programs/`, {
        method: "POST",
        body: program,
        onResponse: async (response) => {
            if (response.response.status == 200) {
                const data: Program = response.response._data;
                if (data.id) {
                    await createDays(data.id);
                    await navigateTo(`/programs/${data.id}`);
                }
            }
        },
    });
}
</script>
