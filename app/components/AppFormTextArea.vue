<template>
    <textarea
        v-model="model"
        class="textarea bg-white text-muted border-2 border-primary-dark rounded-xl focus-within:border-green-500"
    >
    </textarea>
</template>
<script setup lang="ts">
const model = defineModel<string>();
</script>
