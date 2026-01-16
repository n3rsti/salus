<template>
    <Card class="flex flex-col p-3 gap-3">
        <NuxtLink :to="link" class="relative">
            <img
                :src="props.image"
                alt=""
                class="object-cover w-full h-32 rounded-lg shadow border-primary-light border-t-transparent hover:outline-2"
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

            <section class="flex gap-1 flex-wrap mt-auto mb-2">
                <Badge
                    v-for="tag in tags"
                    :key="tag"
                    class="text-xs rounded-md p-0.5 px-1 text-center shadow-xs font-semibold"
                    :class="TagColors[tag]"
                >
                    <Icon :name="TagIcons[tag]" />
                    {{ TagNames[tag] }}</Badge
                >
            </section>

            <slot></slot>
        </div>
    </Card>
</template>
<script setup lang="ts">
import { Card } from "@/components/ui/card";
import { TagColors, TagIcons, TagNames, type Tag } from "~/constants/tags";
import Badge from "./ui/badge/Badge.vue";
const props = defineProps<{
    image?: string;
    title?: string;
    description?: string;
    link?: string;
    tags: Tag[];
    type: "activity" | "program";
}>();
</script>
