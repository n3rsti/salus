<template>
    <nav
        class="p-3 py-1 bg-white shadow-sm flex w-full items-center justify-between h-16 sticky top-0 z-30"
    >
        <NuxtLink to="/">
            <Button
                class="flex items-center gap-1 px-2 justify-center"
                variant="success"
            >
                <Icon
                    class="text-2xl text-white"
                    name="material-symbols:local-fire-department-rounded"
                />
                <span class="shadow-sm font-bold text-white"
                    >{{ streak }}d</span
                >
            </Button>
        </NuxtLink>
        <div
            class="flex items-center h-9 w-full min-w-0 rounded-md px-3 xl:px-6 py-1 text-base shadow-xs md:text-sm bg-white max-xl:mx-3 text-muted-foreground xl:w-2/5 border-input border-2 cursor-text"
            @click="searchStore.open"
        >
            Search...
            <KbdGroup class="ml-auto max-xl:hidden">
                <Kbd>Ctrl</Kbd>
                <span>+</span>
                <Kbd>/</Kbd>
            </KbdGroup>
        </div>
        <Button
            class="border-2 border-primary-dark lg:scale-0 p-2"
            variant="outline"
            lg:disabled
            @click="toggle"
        >
            <Icon class="text-2xl text-green-500" name="ic:round-menu" />
        </Button>
    </nav>
</template>
<script setup lang="ts">
import { useSidebar } from "@/components/ui/sidebar";
import { Button } from "./ui/button";
import { Kbd, KbdGroup } from "./ui/kbd";
import { useMediaQuery } from "@vueuse/core";

const isMobile = useMediaQuery("(max-width: 1024px)");

function toggle() {
    if (isMobile.value == true) {
        toggleSidebar();
    }
}

const searchStore = useSearchStore();

const { toggleSidebar } = useSidebar();

const streak = 7;
</script>
