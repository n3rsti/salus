<template>
    <article
        class="flex flex-col border rounded-xl p-3 bg-primary-light border-neutral-100 border-t border-t-transparent shadow"
    >
        <img
            :src="props.image"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow p-2">
            <h3 class="font-semibold text-text text-lg mt-1">
                {{ props.title }}
            </h3>
            <p class="text-muted text-sm mt-1 mb-4">
                {{ props.description }}
            </p>

            <slot></slot>
        </div>
    </article>
</template>
<script setup lang="ts">
const props = defineProps<{
    image: string;
    title: string;
    description: string;
}>();
</script>
