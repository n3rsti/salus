<template>
    <div>
        <section
            class="w-screen h-screen bg-black/10 fixed z-20 top-0 left-0 transition-opacity lg:hidden"
            :class="props.isOpen ? '' : 'scale-0 opacity-0'"
            @click="toggleSidebar"
        ></section>
        <aside
            class="h-screen fixed z-30 lg:z-0 left-0 top-0 w-60 bg-white transition-transform duration-200 lg:mt-20"
            :class="props.isOpen ? '' : '-translate-x-full lg:translate-0'"
        >
            <section
                class="w-full p-3 lg:p-4 py-5 text-green-600 flex items-center justify-between border-b border-b-green-500 lg:hidden"
            >
                <div>
                    <h3 class="font-bold text-xl">
                        {{ faker.person.firstName() }}
                    </h3>
                    <p class="text-xs text-muted/80 mt-1">View profile</p>
                </div>
                <AppButton
                    class="flex items-center border-green-400 shadow-none rounded-xl py-1"
                    :color="'green'"
                >
                    <Icon
                        class="text-2xl text-white"
                        name="material-symbols:local-fire-department-rounded"
                    />
                    <span class="shadow-sm font-bold text-white"
                        >{{ streak }}d</span
                    >
                </AppButton>
            </section>
            <section class="p-3 lg:p-4 py-5">
                <ul class="flex flex-col gap-2">
                    <li v-for="link in links" :key="link.name">
                        <NuxtLink :to="link.url" @click="toggleSidebar">
                            <AppVerticalCard
                                v-if="link.name"
                                :icon="link.icon || ''"
                                :is-active="isActive(link.url)"
                            >
                                <p class="text-sm">{{ link.name }}</p>
                            </AppVerticalCard>
                            <span
                                v-else
                                class="w-full flex bg-green-500 border-b border-green-400 my-2"
                            ></span>
                        </NuxtLink>
                    </li>
                </ul>
            </section>
        </aside>
    </div>
</template>
<script setup lang="ts">
import { faker } from "@faker-js/faker";

const route = useRoute();

function isActive(path: string | undefined): boolean {
    if (path == undefined) {
        return false;
    }
    return route.path === path;
}

interface Link {
    name?: string;
    url?: string;
    icon?: string;
}

const links: Link[] = [
    {
        name: "Home",
        url: "/",
        icon: "material-symbols:home-rounded",
    },
    {
        name: "In progress",
        icon: "ic:round-timeline",
    },
    {
        name: "Mood log",
        icon: "ic:round-tag-faces",
    },
    {},
    {
        name: "Programs",
        url: "/programs/",
        icon: "ic:round-calendar-month",
    },
    {
        name: "Activities",
        url: "/activities/",
        icon: "ic:round-sports-gymnastics",
    },
];

const streak = 7;

faker.seed(1);
const props = defineProps<{
    isOpen: boolean;
}>();

const emit = defineEmits(["toggleSidebar"]);

function toggleSidebar() {
    emit("toggleSidebar");
}
</script>
