<template>
    <textarea
        v-model="model"
        class="textarea bg-white text-muted placeholder:text-muted/80 border border-primary-dark rounded-xl focus-within:border-green-500 w-full outline-0"
    >
    </textarea>
</template>
<script setup lang="ts">
const model = defineModel<string>();
</script>
