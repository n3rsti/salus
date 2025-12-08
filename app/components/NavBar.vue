<template>
    <nav
        class="p-3 py-1 bg-white shadow-sm flex w-full items-center justify-between z-20"
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
        <Input
            type="search"
            class="bg-white mx-3 text-muted-foreground xl:w-2/5 border-2"
            required
            placeholder="Search"
        />
        <Button
            class="border-2 border-primary-dark lg:scale-0 p-2"
            variant="outline"
            @click="toggleSidebar"
        >
            <Icon class="text-2xl text-green-500" name="ic:round-menu" />
        </Button>
    </nav>
</template>
<script setup>
import { useSidebar } from "@/components/ui/sidebar";
import { Input } from "./ui/input";
import { Button } from "./ui/button";

const { toggleSidebar } = useSidebar();

const streak = 7;
</script>
