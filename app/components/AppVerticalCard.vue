<template>
    <div
        class="px-3 py-2 rounded-lg flex items-center gap-3 cursor-pointer transition-colors"
        :class="
            props.isActive
                ? 'bg-green-500 text-white font-bold'
                : 'text-text hover:bg-green-100'
        "
    >
        <Icon
            :name="props.icon"
            class="text-2xl"
            :class="props.isActive ? 'text-white' : 'text-green-500'"
        />
        <slot />
    </div>
</template>
<script setup lang="ts">
const props = defineProps<{
    isActive?: boolean;
    icon: string;
}>();
</script>
