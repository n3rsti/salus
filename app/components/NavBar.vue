<template>
    <nav class="p-4 bg-white shadow-sm flex items-center">
        <h1 class="text-green-600 font-semibold text-2xl">Salus</h1>
        <p class="ml-auto">
            🔥
            <span
                class="bg-green-300 border-green-800 px-3 py-1 rounded-md text-green-900 shadow-sm font-bold"
                >{{ streak }}d</span
            >
        </p>
    </nav>
</template>
<script setup>
const streak = 7;
</script>
