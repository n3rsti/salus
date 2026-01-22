<template>
    <AppCard
        :image="'/media/' + props.activity.image_url"
        :link="'/activities/' + props.activity.id"
        :title="props.activity.name"
        :description="props.activity.description"
        :type="'activity'"
        :tags="props.activity.tags || []"
        :is-verified="props.activity.owner?.role_id == Role.Trainer"
    >
        <template #type>Activity</template>

        <div class="flex items-center justify-between">
            <p class="text-muted-foreground text-xs flex items-center gap-1">
                <Icon name="ic:outline-access-time" />
                {{ props.activity.duration_minutes }}
                minutes
            </p>
            <p class="text-sm flex items-center text-primary gap-1">
                <template v-if="props.activity.average_rating">
                    <Icon
                        name="material-symbols:star-rounded"
                        class="text-yellow-400 text-xl"
                    />
                    <p class="text-xs font-medium">
                        {{ props.activity.average_rating.toFixed(1) }}
                    </p>
                </template>
                <template v-else>
                    <span class="text-muted-foreground text-xs">No rating</span>
                </template>
            </p>
        </div>
    </AppCard>
</template>
<script setup lang="ts">
import { Role } from "~/constants/roles";
import type { Activity } from "~/models/activity.model";

const props = defineProps<{
    activity: Activity;
}>();
</script>
