<template>
    <Card class="flex flex-col p-3 gap-3">
        <img
            :src="props.image"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow">
            <h3 class="font-semibold text-text text-lg mt-1">
                {{ props.title }}
            </h3>
            <small class="mt-1 mb-4">
                {{ props.description }}
            </small>

            <slot></slot>
        </div>
    </Card>
</template>
<script setup lang="ts">
import { Button } from "@/components/ui/button";
import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
const props = defineProps<{
    image?: string;
    title?: string;
    description?: string;
}>();
</script>
