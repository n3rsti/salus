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
                        <Button variant="outline"> Open Dialog </Button>
                    </DialogTrigger>
                    <DialogContent class="sm:max-w-[425px]">
                        <DialogHeader>
                            <DialogTitle>Edit profile</DialogTitle>
                            <DialogDescription>
                                Make changes to your profile here. Click save
                                when you're done.
                            </DialogDescription>
                        </DialogHeader>
                        <div class="grid gap-4">
                            <div class="grid gap-3">
                                <Label for="name-1">Name</Label>
                                <Input
                                    id="name-1"
                                    name="name"
                                    default-value="Pedro Duarte"
                                />
                            </div>
                            <div class="grid gap-3">
                                <Label for="username-1">Username</Label>
                                <Input
                                    id="username-1"
                                    name="username"
                                    default-value="@peduarte"
                                />
                            </div>
                        </div>
                        <DialogFooter>
                            <DialogClose as-child>
                                <Button variant="outline"> Cancel </Button>
                            </DialogClose>
                            <Button type="submit"> Save changes </Button>
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
                        <AppFormLabel for="name">Name</AppFormLabel>
                        <AppFormInput
                            id="name"
                            v-model="activity.name"
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
                        <AppFormLabel for="duration"
                            >Duration
                            <span class="text-muted/70 text-xs"
                                >(minutes)</span
                            ></AppFormLabel
                        >
                        <AppFormInput
                            id="duration"
                            v-model="activity.duration"
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
                            v-model="activity.image_url"
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
                                    activity.difficulty == difficulty.value
                                        ? difficulty.classes.border
                                        : 'border-primary-dark font-light'
                                "
                            >
                                <input
                                    :id="difficulty.name.toLowerCase()"
                                    v-model="activity.difficulty"
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
                    >Submit</AppButton
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
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { Activity } from "~/models/activity.model";

const route = useRoute();

const props = defineProps<{
    activity: Activity;
}>();

const emits = defineEmits<{
    update: [activity: Activity];
}>();

const activity = ref(props.activity);

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

async function submitForm() {
    emits("update", activity.value);
}
</script>
