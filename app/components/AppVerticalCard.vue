<template>
    <Card
        class="flex flex-col w-full gap-2 p-3 border border-primary-dark rounded-xl hover:outline"
    >
        <div class="flex items-center w-full gap-2">
            <img
                :src="'/media/' + props.img"
                alt=""
                class="h-8 aspect-square rounded-lg"
            />
            <p class="text-primary font-medium text-sm hover:underline py-1">
                <slot name="name"></slot>
            </p>

            <slot name="badge"></slot>
        </div>
        <div class="w-full">
            <p class="text-muted-foreground text-xs">
                <slot name="description"></slot>
            </p>
        </div>
    </Card>
</template>
<script setup lang="ts">
import { Card } from "./ui/card";

const props = defineProps<{
    img: string;
}>();
</script>
