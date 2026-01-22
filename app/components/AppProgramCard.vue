<template>
    <AppCard
        :image="'/media/' + props.program.image_url"
        :title="props.program.name"
        :description="props.program.description"
        :link="'/programs/' + props.program.id"
        :type="'program'"
        :tags="props.program.tags || []"
        :is-verified="props.program.owner?.role_id == Role.Trainer"
    >
        <template #type>Program</template>
        <div
            v-if="props.program.progress"
            class="flex items-center justify-between mt-auto"
        >
            <p
                class="font-medium text-muted-foreground text-sm flex items-center gap-1"
            >
                <Icon name="ic:baseline-calendar-month" />
                Day
                {{
                    faker.number.int({
                        min: 1,
                        max: props.program.duration_days,
                    })
                }}/{{ props.program.duration_days }}
            </p>
            <p class="text-sm flex items-center text-green-500 gap-1">
                {{ props.program.progress }}%
            </p>
        </div>

        <div v-else class="flex items-center justify-between">
            <p class="text-muted-foreground text-xs flex items-center gap-1">
                <Icon name="ic:outline-access-time" />
                {{ props.program.duration_days }}
                days
            </p>
            <p class="text-sm flex items-center text-primary">
                <template v-if="props.program.average_rating">
                    <Icon
                        name="material-symbols:star-rounded"
                        class="text-yellow-400 text-xl"
                    />
                    <p class="text-xs font-medium">
                        {{ props.program.average_rating.toFixed(1) }}
                    </p>
                </template>
                <template v-else>
                    <span class="text-muted-foreground text-xs">No rating</span>
                </template>
            </p>
        </div>

        <progress
            v-if="props.program.progress"
            class="progress progress-success w-full mt-4"
            :value="props.program.progress"
            max="100"
        ></progress>
    </AppCard>
</template>
<script setup lang="ts">
import { faker } from "@faker-js/faker";
import { Role } from "~/constants/roles";
import type { Program } from "~/models/program.model";

const props = defineProps<{
    program: Program;
}>();
</script>
