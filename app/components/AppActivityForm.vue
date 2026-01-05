<template>
    <div>
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">
                <template v-if="route.params.id"> Update activity </template>
                <template v-else> Create activity </template>
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
                                Are you sure you want to delete activity
                                <span class="font-bold text-primary">
                                    {{ activity.name }}
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
                                @click="emits('delete')"
                                >Delete</Button
                            >
                        </DialogFooter>
                    </DialogContent>
                </form>
            </Dialog>
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
                        <Label for="name">Name</Label>
                        <Input
                            id="name"
                            v-model="activity.name"
                            type="text"
                            placeholder="Enter name"
                            required
                        />
                    </div>
                    <div class="flex flex-col gap-2 flex-1 min-h-0">
                        <Label for="description">Description</Label>

                        <Textarea
                            id="description"
                            v-model="activity.description"
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
                        <Label for="duration"
                            >Duration
                            <span class="text-muted/70 text-xs"
                                >(minutes)</span
                            ></Label
                        >
                        <Input
                            id="duration"
                            v-model="activity.duration_minutes"
                            type="number"
                            min="0"
                            required
                        />
                    </div>
                    <div class="flex flex-col gap-2">
                        <Label for="image"
                            >Image
                            <span class="text-muted/70 text-xs"
                                >(url)</span
                            ></Label
                        >
                        <input
                            id="image"
                            ref="fileInput"
                            type="file"
                            name="image"
                            accept="image/*"
                            :required="route.params.id == undefined"
                        />
                    </div>

                    <div class="flex flex-col gap-2">
                        <FieldGroup>
                            <FieldSet>
                                <FieldLabel for="compute-environment-p8w">
                                    Difficulty
                                </FieldLabel>
                                <FieldDescription>
                                    Select the compute environment for your
                                    cluster.
                                </FieldDescription>
                                <RadioGroup v-model="activity.difficulty">
                                    <FieldLabel
                                        v-for="difficulty in difficulties"
                                        :key="difficulty.name"
                                        :for="difficulty.name.toLowerCase()"
                                    >
                                        <Field orientation="horizontal">
                                            <FieldContent>
                                                <FieldTitle>{{
                                                    difficulty.name
                                                }}</FieldTitle>
                                                <FieldDescription>
                                                    {{ difficulty.description }}
                                                </FieldDescription>
                                            </FieldContent>
                                            <RadioGroupItem
                                                :id="
                                                    difficulty.name.toLowerCase()
                                                "
                                                name="difficulty"
                                                :value="difficulty.value"
                                            />
                                        </Field>
                                    </FieldLabel>
                                </RadioGroup>
                            </FieldSet>
                        </FieldGroup>
                    </div>
                </div>
                <Button
                    type="submit"
                    variant="success"
                    class="w-full md:col-span-2"
                    >Submit</Button
                >
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Button } from "@/components/ui/button";
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

import {
    Field,
    FieldContent,
    FieldDescription,
    FieldGroup,
    FieldLabel,
    FieldSet,
    FieldTitle,
} from "@/components/ui/field";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Input } from "@/components/ui/input";
import { Label as Label } from "@/components/ui/label";
import type { Activity } from "~/models/activity.model";
import { Textarea } from "./ui/textarea";

const route = useRoute();

const props = defineProps<{
    activity: Activity;
}>();

const emits = defineEmits<{
    submit: [activity: Activity, file: File | undefined];
    delete: [];
}>();

const activity = ref(props.activity);

const fileInput = ref<HTMLInputElement | null>(null);

interface Difficulty {
    name: string;
    value: number;
    description?: string;
    classes: Record<string, string>;
}

const difficulties: Difficulty[] = [
    {
        name: "Easy",
        value: 1,
        description: "Doable for everyone",
        classes: {
            radio: "radio-success",
            text: "text-success",
            border: "border-success",
        },
    },
    {
        name: "Moderate",
        value: 2,
        description: "Harder, but doable for the majority",
        classes: {
            radio: "radio-info",
            text: "text-info",
            border: "border-info",
        },
    },
    {
        name: "Hard",
        value: 3,
        description: "Fitness level required",
        classes: {
            radio: "radio-error",
            text: "text-error",
            border: "border-error",
        },
    },
];

async function submitForm() {
    const file = fileInput.value?.files?.[0];
    emits("submit", activity.value, file);
}
</script>
