<template>
    <nav class="p-4 bg-white shadow-sm flex items-center">
        <AppButton
            class="flex items-center bg-green-500 border-green-400 shadow-green-400 rounded-xl"
        >
            <Icon
                class="text-2xl text-green-100"
                name="material-symbols:local-fire-department-rounded"
            />
            <span class="shadow-sm font-bold text-green-100"
                >{{ streak }}d</span
            >
        </AppButton>
        <AppButton class="ml-auto border-0 inset-shadow-sm">
            <Icon class="text-2xl text-green-500" name="ic:round-menu" />
        </AppButton>
    </nav>
</template>
<script setup>
const streak = 7;
</script>
