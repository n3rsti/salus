<template>
    <AppCard
        :image="props.activity.image"
        :title="props.activity.name"
        :description="props.activity.description"
    >
        <div class="flex items-center justify-between mt-auto">
            <p class="text-muted/90 text-sm flex items-center gap-1">
                <Icon name="ic:outline-access-time" />
                {{ props.activity.duration_minutes }}
                minutes
            </p>
            <p class="text-sm flex items-center text-text gap-1">
                {{ props.activity.rating }}/5
                <Icon
                    name="material-symbols:star-rounded"
                    class="text-yellow-400 text-2xl"
                />
            </p>
        </div>
        <AppButton
            class="w-full shadow-sm border-t-transparent text-white mt-3"
            :color="'green_dark'"
        >
            View info
            <Icon class="text-lg ml-2" name="ic:round-remove-red-eye" />
        </AppButton>
    </AppCard>
</template>
<script setup lang="ts">
import type { Activity } from "~/models/activity.model";

const props = defineProps<{
    activity: Activity;
}>();
</script>
