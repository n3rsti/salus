<template>
    <input
        v-model="model"
        class="input bg-white text-muted border-2 border-primary-dark rounded-xl focus-within:border-green-500"
    />
</template>
<script setup lang="ts">
const model = defineModel<string>();
</script>
