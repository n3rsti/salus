<template>
    <div :class="searchStore.isOpen ? '' : 'scale-0'">
        <div
            class="w-full h-full fixed top-0 left-0 bg-black/20 z-20"
            @click="searchStore.close"
        ></div>
        <Card
            class="max-h-screen fixed top-5 left-1/2 -translate-x-1/2 z-20 px-2 pt-2 gap-3"
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
                <slot name="loading">
                    <Skeleton v-for="n in 3" :key="n" class="h-10 w-full" />
                </slot>
            </div>
            <div v-else-if="notFound" class="text-center py-2">
                <h2 class="font-semibold">Not found...</h2>
                <p class="text-sm">
                    <slot name="not-found" />
                </p>
            </div>
            <div v-else class="flex flex-col gap-2 py-1">
                <slot name="results">
                    <slot name="default" />
                </slot>
            </div>
        </Card>
    </div>
</template>

<script setup lang="ts">
import { Card } from "./ui/card";
import { Input } from "./ui/input";
import { Skeleton } from "./ui/skeleton";

import { onKeyStroke, watchDebounced } from "@vueuse/core";

const searchStore = useSearchStore();

const props = defineProps<{
    notFound: boolean;
    isLoading: boolean;
    resetKey: number;
}>();

const emit = defineEmits<{
    clear: [];
    fetch: [input: string, controller: AbortController];
}>();

const searchInput = ref("");

const searchInputRef = ref<typeof HTMLInputElement | null>(null);

watch(
    () => searchStore.isOpen,
    async (isOpen) => {
        if (!isOpen) return;

        await nextTick();
        setTimeout(() => {
            searchInputRef.value?.$el.focus();
        }, 100);
    },
);

watch(
    () => props.resetKey,
    () => {
        searchInput.value = "";
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
        newValue = newValue.trim();
        if (!newValue) {
            emit("clear");
            return;
        }

        const controller = new AbortController();
        onCleanup(() => controller.abort());

        emit("fetch", newValue, controller);
    },
    { debounce: 250, maxWait: 3000 },
);
</script>
