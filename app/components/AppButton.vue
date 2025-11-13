<template>
    <button
        class="p-2 rounded-md border font-semibold text-sm cursor-pointer flex items-center justify-center transition-all"
        :class="styles[color]"
    >
        <slot></slot>
    </button>
</template>

<script setup lang="ts">
const props = defineProps<{
    color?: string;
}>();

const styles: Record<string, string[]> = {
    green: [
        "bg-green-500 border-green-300 shadow-green-300 hover:bg-green-600 hover:shadow-none",
    ],
    green_dark: [
        "bg-green-600 border-green-400 shadow-green-400 hover:bg-green-700 hover:shadow-none",
    ],
    blue: [
        "bg-info border-info shadow-info hover:bg-blue-500 hover:shadow-none",
    ],
    black: [
        "bg-text border-text/90 shadow-text/90 hover:bg-text/90 hover:shadow-none",
    ],
    red: [
        "bg-red-500 border-red-300 shadow-red-300 hover:bg-red-600 hover:shadow-none",
    ],
    "": [],
};

const color = props.color || "";
</script>
