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
                    <li>
                        <NuxtLink to="/">
                            <AppVerticalCard
                                :icon="'material-symbols:home-rounded'"
                                :is-active="true"
                            >
                                <p>Home</p>
                            </AppVerticalCard>
                        </NuxtLink>
                    </li>
                    <li>
                        <NuxtLink to="/">
                            <AppVerticalCard :icon="'ic:round-timeline'">
                                <p>In progress</p>
                            </AppVerticalCard>
                        </NuxtLink>
                    </li>
                    <li>
                        <NuxtLink to="/">
                            <AppVerticalCard :icon="'ic:round-tag-faces'">
                                <p>Mood log</p>
                            </AppVerticalCard>
                        </NuxtLink>
                    </li>
                </ul>
                <span
                    class="w-full flex bg-green-500 border-b border-green-400 my-2"
                ></span>
                <ul class="flex flex-col gap-1">
                    <li>
                        <NuxtLink to="/">
                            <AppVerticalCard :icon="'ic:round-calendar-month'">
                                <p>Programs</p>
                            </AppVerticalCard>
                        </NuxtLink>
                    </li>
                    <li>
                        <NuxtLink to="/">
                            <AppVerticalCard
                                :icon="'ic:round-sports-gymnastics'"
                            >
                                <p>Activities</p>
                            </AppVerticalCard>
                        </NuxtLink>
                    </li>
                </ul>
            </section>
        </aside>
    </div>
</template>
<script setup lang="ts">
import { faker } from "@faker-js/faker";

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
