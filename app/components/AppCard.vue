<template>
    <Card class="flex flex-col p-3 gap-3">
        <img
            :src="props.image"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow">
            <h3 class="font-semibold text-text mt-1 leading-none">
                {{ props.title }}
            </h3>
            <small
                v-if="props.description"
                class="mt-1 mb-4 text-xs text-muted-foreground line-clamp-2"
                :title="props.description"
            >
                {{ props.description }}
            </small>

            <slot></slot>
        </div>
    </Card>
</template>
<script setup lang="ts">
import { Card } from "@/components/ui/card";
const props = defineProps<{
    image?: string;
    title?: string;
    description?: string;
}>();
</script>
