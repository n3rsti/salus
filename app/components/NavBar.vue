<template>
    <nav class="p-4 bg-white shadow-sm flex items-center">
        <AppButton
            class="flex items-center bg-green-500 border-green-400 shadow-none rounded-xl py-1"
        >
            <Icon
                class="text-2xl text-green-100"
                name="material-symbols:local-fire-department-rounded"
            />
            <span class="shadow-sm font-bold text-green-100"
                >{{ streak }}d</span
            >
        </AppButton>
        <label
            class="input bg-white mx-3 text-muted border-primary-dark rounded-xl"
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
        <AppButton class="ml-auto border-primary-dark rounded-xl">
            <Icon class="text-2xl text-green-500" name="ic:round-menu" />
        </AppButton>
    </nav>
</template>
<script setup>
const streak = 7;
</script>
