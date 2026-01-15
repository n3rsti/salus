<template>
    <Card class="flex flex-col p-3 gap-3">
        <NuxtLink :to="link">
            <img
                :src="props.image"
                alt=""
                class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent hover:outline-2"
            />
        </NuxtLink>
        <div class="flex flex-col grow">
            <NuxtLink :to="link">
                <h3
                    class="font-semibold text-text mt-1 leading-none hover:underline"
                >
                    {{ props.title }}
                </h3>
            </NuxtLink>
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
    link?: string;
}>();
</script>
