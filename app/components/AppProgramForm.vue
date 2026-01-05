<template>
    <div>
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">
                {{ route.params.id ? "Edit" : "Create" }} program
            </h1>

            <Dialog v-if="route.params.id">
                <form>
                    <DialogTrigger as-child>
                        <Button variant="destructive">Delete</Button>
                    </DialogTrigger>
                    <DialogContent class="sm:max-w-[425px]">
                        <DialogHeader>
                            <DialogTitle>Delete activity</DialogTitle>
                            <DialogDescription>
                                Are you sure you want to delete program
                                <span class="font-bold text-primary">
                                    {{ initialData?.name }}
                                </span>
                            </DialogDescription>
                        </DialogHeader>
                        <DialogFooter>
                            <DialogClose as-child>
                                <Button variant="outline"> Cancel </Button>
                            </DialogClose>
                            <Button
                                type="submit"
                                variant="destructive"
                                @click="emit('delete')"
                                >Delete</Button
                            >
                        </DialogFooter>
                    </DialogContent>
                </form>
            </Dialog>
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
                        <Label for="name">Name</Label>
                        <Input
                            id="name"
                            v-model="formData.name"
                            type="text"
                            placeholder="Enter name"
                            required
                        />
                    </div>
                    <div class="flex flex-col gap-2">
                        <Label for="description">Description</Label>
                        <Textarea
                            id="description"
                            v-model="formData.description"
                            name="description"
                            placeholder="Describe your program..."
                            required
                        ></Textarea>
                    </div>
                    <div class="flex flex-col gap-2">
                        <Label for="image"
                            >Image
                            <span class="text-muted-foreground text-xs"
                                >(file)</span
                            ></Label
                        >
                        <input
                            id="image"
                            ref="fileInput"
                            type="file"
                            name="image"
                            accept="image/*"
                            class="file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground dark:bg-input/30 border-input h-9 w-full min-w-0 rounded-md border bg-transparent px-3 py-1 text-base shadow-xs transition-[color,box-shadow] outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive"
                            :required="route.params.id == undefined"
                        />
                    </div>
                </div>
                <div
                    class="flex flex-col gap-3 bg-primary-light shadow-sm p-4 rounded-xl"
                >
                    <div
                        v-for="day in formData.days"
                        :key="day.day_number"
                        class="rounded-xl border-primary-dark border collapse collapse-arrow shadow-inner"
                    >
                        <input type="checkbox" checked />
                        <div class="collapse-title font-semibold text-text">
                            Day {{ day.day_number }}
                        </div>
                        <div class="px-4 collapse-content flex flex-col gap-3">
                            <div class="flex flex-col gap-2">
                                <Label :for="day.day_number + '-description'"
                                    >Description</Label
                                >
                                <Textarea
                                    :id="day.day_number + '-description'"
                                    v-model="day.description"
                                    class="focus:border-text"
                                    placeholder="Describe the day..."
                                    required
                                ></Textarea>
                            </div>

                            <div class="flex flex-col gap-2">
                                <Label :for="day.day_number + '-activities'"
                                    >Add activities</Label
                                >
                                <div class="flex gap-2">
                                    <Input
                                        :id="day.day_number + '-activities'"
                                        v-model="activityInputs[day.day_number]"
                                        type="number"
                                        min="1"
                                        placeholder="Enter activity id"
                                        class="focus:border-text"
                                    />
                                    <Button
                                        class="w-1/4 rounded-lg bg-text text-xs"
                                        variant="default"
                                        type="button"
                                        @click="
                                            addActivity(
                                                activityInputs[day.day_number],
                                                day.day_number,
                                            )
                                        "
                                        >Add</Button
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
                                    <Button
                                        variant="destructive"
                                        class="ml-auto btn-xs text-xs"
                                        @click="
                                            removeActivity(
                                                activity.id,
                                                day.day_number,
                                            )
                                        "
                                        >Remove</Button
                                    >
                                </div>
                                <div class="w-full">
                                    <p class="text-muted-foreground text-xs">
                                        {{ activity.description }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <Button
                        class="text-xs mt-auto"
                        variant="default"
                        type="button"
                        @click="addDay"
                        >Add day</Button
                    >
                </div>

                <Button
                    type="submit"
                    variant="success"
                    class="w-full mt-3 md:col-span-2"
                    >Submit</Button
                >
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Button } from "~/components/ui/button";
import type { Program } from "~/models/program.model";
import type { ProgramDay } from "~/models/program_day.model";

import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";

import { Input } from "@/components/ui/input";
import { Label as Label } from "@/components/ui/label";
import type { Activity } from "~/models/activity.model";
import { Textarea } from "./ui/textarea";

const route = useRoute();

const props = defineProps<{
    initialData?: Program;
}>();

const emit = defineEmits<{
    submit: [program: Program, file: File | undefined];
    delete: [];
}>();

const fileInput = ref<HTMLInputElement | null>(null);

const formData = ref<Program>({
    name: props.initialData?.name || "",
    description: props.initialData?.description || "",
    duration_days: props.initialData?.duration_days || 1,
    image_url: props.initialData?.image_url || "",
    language: props.initialData?.language || "pl",
    days: props.initialData?.days || [
        {
            day_number: 1,
            description: "",
            program_id: props.initialData?.id || 0,
            activities: [],
        },
    ],
});

const activityInputs = ref<Record<number, number | undefined>>({});

function removeActivity(activity_id: number | undefined, dayNumber: number) {
    if (activity_id === undefined) return;

    const day = formData.value.days?.find((d) => d.day_number === dayNumber);
    if (day && day.activities) {
        day.activities = day.activities.filter((a) => a.id !== activity_id);
    }
}

async function addActivity(activity_id: number | undefined, dayNumber: number) {
    if (activity_id === undefined) return;

    const day = formData.value.days?.find((d) => d.day_number === dayNumber);
    if (!day) return;

    const isAlreadyAdded = day.activities?.some((a) => a.id === activity_id);
    if (isAlreadyAdded) {
        activityInputs.value[dayNumber] = undefined;
        return;
    }

    try {
        const data = await $fetch<Activity>(`/api/activities/${activity_id}/`);

        if (!day.activities) {
            day.activities = [];
        }
        day.activities.push(data);
        activityInputs.value[dayNumber] = undefined;
    } catch (error) {
        console.error("Failed to fetch activity:", error);
    }
}

function addDay() {
    if (!formData.value.days) {
        formData.value.days = [];
    }

    const newDay: ProgramDay = {
        day_number: formData.value.days.length + 1,
        description: "",
        program_id: formData.value.id || 0,
        activities: [],
    };

    formData.value.days.push(newDay);
    formData.value.duration_days = formData.value.days.length;
}

async function submitForm() {
    formData.value.days?.forEach((day) => {
        day.activities_ids =
            day.activities
                ?.map((a) => a.id)
                .filter((id): id is number => id !== undefined) || [];
    });

    const programToSubmit: Program = {
        ...formData.value,
        duration_days: formData.value.days?.length || 0,
    };

    const file = fileInput.value?.files?.[0];

    emit("submit", programToSubmit, file);
}
</script>
