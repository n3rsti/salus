<template>
    <AppCard
        :image="props.program.image"
        :title="props.program.name"
        :description="props.program.description"
    >
        <div
            v-if="props.program.progress"
            class="flex items-center justify-between mt-auto"
        >
            <p
                class="font-medium text-muted/90 text-sm flex items-center gap-1"
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

        <div v-else class="flex items-center justify-between mt-auto">
            <p class="text-muted/90 text-sm flex items-center gap-1">
                <Icon name="ic:outline-access-time" />
                {{ props.program.duration_days }}
                days
            </p>
            <p class="text-sm flex items-center text-text gap-1">
                {{ props.program.rating || 0 }}/5
                <Icon
                    name="material-symbols:star-rounded"
                    class="text-yellow-400 text-2xl"
                />
            </p>
        </div>

        <progress
            v-if="props.program.progress"
            class="progress progress-success w-full mt-4"
            :value="props.program.progress"
            max="100"
        ></progress>

        <AppButton
            v-if="props.program.progress"
            class="w-full shadow-sm border-t-transparent text-white mt-3"
            :color="'green'"
        >
            Continue

            <Icon class="text-lg ml-2" name="ic:round-play-arrow" />
        </AppButton>
        <AppButton
            v-else
            class="w-full shadow-sm border-t-transparent text-white mt-3"
            :color="'green_dark'"
        >
            View info
            <Icon class="text-lg ml-2" name="ic:round-remove-red-eye" />
        </AppButton>
    </AppCard>
</template>
<script setup lang="ts">
import { faker } from "@faker-js/faker";
import type { Program } from "~/models/program.model";

const props = defineProps<{
    program: Program;
}>();
</script>
