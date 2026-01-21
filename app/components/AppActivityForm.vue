<template>
    <div>
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">
                <template v-if="activityId"> Update activity </template>
                <template v-else> Create activity </template>
            </h1>
            <Dialog
                v-if="
                    (activityId && userStore.id == activity.owner?.id) ||
                    userStore.isAdmin()
                "
            >
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
                            :disabled="
                                userStore.isAdmin() && activityId != undefined
                            "
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
                            :disabled="
                                userStore.isAdmin() && activityId != undefined
                            "
                            required
                        />
                    </div>
                    <div class="flex flex-col gap-2 flex-1 min-h-0">
                        <Label for="description">Content</Label>

                        <Textarea
                            id="content"
                            v-model="activity.content"
                            class="md:flex-1 md:min-h-0"
                            name="content"
                            placeholder="Add instructions..."
                            :disabled="
                                userStore.isAdmin() && activityId != undefined
                            "
                            required
                        />
                    </div>

                    <div class="flex flex-col gap-2">
                        <AppTagInput
                            :selected-tags="activity.tags"
                            :disabled="
                                userStore.isAdmin() && activityId != undefined
                            "
                            @update-tags="updateTags"
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
                            :disabled="
                                userStore.isAdmin() && activityId != undefined
                            "
                            required
                        />
                    </div>
                    <div class="flex flex-col gap-2">
                        <Label for="image"
                            >Image
                            <span class="text-muted/70 text-xs"
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
                            :disabled="
                                userStore.isAdmin() && activityId != undefined
                            "
                            :required="activityId == undefined"
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
                                <RadioGroup
                                    v-model="activity.difficulty"
                                    :disabled="
                                        userStore.isAdmin() &&
                                        activityId != undefined
                                    "
                                >
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
                    :disabled="userStore.isAdmin() && activityId != undefined"
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
import type { Tag } from "~/constants/tags";

const route = useRoute();
const activityId = route.params.id;
const userStore = useUserStore();

const props = defineProps<{
    activity: Activity;
}>();

const emits = defineEmits<{
    submit: [activity: Activity, file: File | undefined];
    updateTags: [tags: Tag[]];
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

function updateTags(tags: Tag[]) {
    activity.value.tags = tags;
}
</script>
