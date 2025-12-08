<template>
    <AppCard
        :image="props.activity.image_url"
        :title="props.activity.name"
        :description="props.activity.description"
    >
        <div class="flex items-center justify-between mt-auto">
            <p class="text-muted-foreground text-sm flex items-center gap-1">
                <Icon name="ic:outline-access-time" />
                {{ props.activity.duration_minutes }}
                minutes
            </p>
            <p class="text-sm flex items-center text-text gap-1">
                <template v-if="props.activity.rating">
                    {{ props.activity.rating }}/5
                    <Icon
                        name="material-symbols:star-rounded"
                        class="text-yellow-400 text-2xl"
                    />
                </template>
                <template v-else>
                    <span class="text-muted-foreground text-xs">No rating</span>
                </template>
            </p>
        </div>

        <NuxtLink :to="'/activities/' + props.activity.id">
            <Button class="w-full mt-3" variant="success_shadow">
                View info
                <Icon class="text-lg ml-2" name="ic:round-remove-red-eye" />
            </Button>
        </NuxtLink>
    </AppCard>
</template>
<script setup lang="ts">
import type { Activity } from "~/models/activity.model";
import { Button } from "./ui/button";

const props = defineProps<{
    activity: Activity;
}>();
</script>
