<template>
    <div :class="searchStore.isOpen ? '' : 'scale-0'">
        <div
            class="w-full h-full fixed top-0 left-0 bg-black/20 z-20"
            @click="searchStore.close"
        ></div>
        <Card
            class="fixed top-20 left-1/2 -translate-x-1/2 z-20 px-2 pt-2 gap-3"
        >
            <Input
                ref="searchInputRef"
                v-model="searchInput"
                type="search"
                class="bg-white text-muted-foreground w-[90vw] md:w-[70vw] xl:w-[50vw] border-2 px-3 py-5"
                required
                placeholder="Search"
            />

            <div v-if="isLoading" class="flex flex-col gap-2">
                <div class="flex flex-col rounded-md py-2 px-2 gap-2">
                    <div class="flex items-center gap-2">
                        <Skeleton class="h-8 aspect-square rounded-lg" />
                        <Skeleton class="w-20 h-4 rounded-md" />
                        <Skeleton class="w-12 h-5 rounded-md" />
                        <Skeleton class="ml-auto w-20 h-5 rounded-md" />
                    </div>
                    <Skeleton class="w-full h-5 rounded-md" />
                </div>
            </div>
            <div v-else-if="notFound" class="text-green-500 text-center">
                <Icon
                    class="text-6xl"
                    name="material-symbols:sports-gymnastics"
                />
                <h2 class="text-sm font-semibold">Not found...</h2>
            </div>
            <div v-else-if="activities.length == 0">
                <h2 class="text-sm text-center">Search for stuff</h2>
            </div>
            <div v-else class="flex flex-col gap-2">
                <NuxtLink
                    v-for="activity in activities"
                    :key="activity.id"
                    :to="'/activities/' + activity.id"
                    class="py-2 px-2 rounded-md border flex flex-col gap-2 hover:bg-accent transition-colors shadow-xs"
                    @click="close"
                >
                    <div class="flex items-center gap-2">
                        <img
                            :src="activity.image_url"
                            alt=""
                            class="h-8 aspect-square rounded-lg"
                        />
                        <h3
                            class="font-semibold text-sm hover:underline cursor-pointer"
                        >
                            {{ activity.name }}
                        </h3>
                        <Badge
                            class="text-xs rounded-md"
                            :class="DifficultiesColors[activity.difficulty]"
                            >{{ Difficulties[activity.difficulty] }}</Badge
                        >
                        <span class="flex items-center ml-auto text-xs gap-1">
                            <Icon name="ic:outline-access-time" />
                            {{ activity.duration_minutes }} minutes
                        </span>
                    </div>
                    <p class="text-sm text-accent-content">
                        {{ activity.description }}
                    </p>
                </NuxtLink>

                <NuxtLink
                    v-for="program in programs"
                    :key="program.id"
                    :to="'/programs/' + program.id"
                    class="py-2 px-2 rounded-md border flex flex-col gap-2 hover:bg-accent transition-colors shadow-xs"
                    @click="close"
                >
                    <div class="flex items-center gap-2">
                        <img
                            :src="program.image_url"
                            alt=""
                            class="h-8 aspect-square rounded-lg"
                        />
                        <h3
                            class="font-semibold text-sm hover:underline cursor-pointer"
                        >
                            {{ program.name }}
                        </h3>
                        <span class="flex items-center ml-auto text-xs gap-1">
                            <Icon name="ic:outline-access-time" />
                            {{ program.duration_days }} days
                        </span>
                    </div>
                    <p class="text-sm text-accent-content">
                        {{ program.description }}
                    </p>
                </NuxtLink>
            </div>
        </Card>
    </div>
</template>

<script setup lang="ts">
import type { Activity } from "~/models/activity.model";
import { Card } from "./ui/card";
import { Input } from "./ui/input";
import { Badge } from "./ui/badge";
import { Difficulties, DifficultiesColors } from "~/constants/difficulty";
import type { Program } from "~/models/program.model";
import { Skeleton } from "./ui/skeleton";

import { onKeyStroke, watchDebounced } from "@vueuse/core";

const { $api } = useNuxtApp();
const searchStore = useSearchStore();

const activities = ref<Activity[]>([]);
const programs = ref<Program[]>([]);
const isLoading = ref(false);
const searchInput = ref("");

const notFound = ref(false);

const searchInputRef = ref<typeof HTMLInputElement | null>(null);

function close() {
    searchStore.close();
    searchInput.value = "";
}

watch(
    () => searchStore.isOpen,
    async (isOpen) => {
        if (!isOpen) return;

        await nextTick();
        console.log(searchInputRef.value?.$el.focus());
    },
);

onKeyStroke("Escape", (e) => {
    e.preventDefault();
    searchStore.close();
});

onKeyStroke("/", (e) => {
    if (!(e.ctrlKey || e.metaKey)) return;
    if (searchStore.isOpen) return;

    e.preventDefault();
    searchStore.open();
});

watchDebounced(
    searchInput,
    async (newValue, _oldValue, onCleanup) => {
        notFound.value = false;
        newValue = newValue.trim();
        if (!newValue) {
            activities.value = [];
            programs.value = [];
            return;
        }

        const controller = new AbortController();
        onCleanup(() => controller.abort());

        isLoading.value = true;
        try {
            const [a, p] = await Promise.all([
                $api<Activity[]>(
                    `/api/activities/?search=${encodeURIComponent(newValue)}`,
                    { signal: controller.signal },
                ),
                $api<Program[]>(
                    `/api/programs/?search=${encodeURIComponent(newValue)}`,
                    { signal: controller.signal },
                ),
            ]);

            activities.value = a;
            programs.value = p;

            if (a.length + p.length == 0) notFound.value = true;
        } catch (err: any) {
            if (err?.name !== "AbortError") console.error(err);
        } finally {
            isLoading.value = false;
        }
    },
    { debounce: 250, maxWait: 3000 },
);
</script>
