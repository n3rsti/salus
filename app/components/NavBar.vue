<template>
    <nav
        class="p-4 bg-white shadow-sm flex w-full items-center justify-between"
    >
        <NuxtLink to="/">
            <AppButton
                class="flex items-center border-green-400 shadow-none rounded-xl py-1 lg:p-2 lg:px-3 justify-center"
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
        </NuxtLink>
        <label
            class="input bg-white mx-3 text-muted border-2 border-primary-dark rounded-xl focus-within:border-green-500 xl:w-2/5"
        >
            <svg
                class="h-[1em] opacity-50"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
            >
                <g
                    stroke-linejoin="round"
                    stroke-linecap="round"
                    stroke-width="2.5"
                    fill="none"
                    stroke="currentColor"
                >
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.3-4.3"></path>
                </g>
            </svg>
            <input type="search" required placeholder="Search" />
        </label>
        <AppButton
            class="border-2 border-primary-dark rounded-xl lg:scale-0"
            @click="toggleSidebar"
        >
            <Icon class="text-2xl text-green-500" name="ic:round-menu" />
        </AppButton>
    </nav>
</template>
<script setup>
const streak = 7;

const emit = defineEmits(["toggle_sidebar"]);

function toggleSidebar() {
    emit("toggle_sidebar");
}
</script>
