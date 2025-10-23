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
    "": [],
};

const color = props.color || "";
</script>
