<template>
    <nav
        class="p-4 sm:px-8 md:px-10 lg:px-14 bg-white shadow-sm flex items-center justify-between"
    >
        <AppButton
            class="flex items-center border-green-400 shadow-none rounded-xl py-1"
            :color="'green'"
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
        <AppButton class="border-2 border-primary-dark rounded-xl lg:scale-0">
            <Icon class="text-2xl text-green-500" name="ic:round-menu" />
        </AppButton>
    </nav>
</template>
<script setup>
const streak = 7;
</script>
