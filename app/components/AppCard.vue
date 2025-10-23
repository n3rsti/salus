<template>
    <article
        class="flex flex-col border rounded-xl p-3 bg-primary-light border-neutral-100 border-t border-t-transparent shadow"
    >
        <img
            :src="props.data?.image"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow p-2">
            <h3 class="font-semibold text-text text-lg mt-1">
                {{ props.data?.name }}
            </h3>
            <p class="text-muted text-sm mt-1 mb-4">
                {{ props.data?.description }}
            </p>

            <div
                v-if="isInProgress"
                class="flex items-center justify-between mt-auto"
            >
                <p
                    v-if="props.data?.duration"
                    class="font-medium text-muted/90 text-sm flex items-center gap-1"
                >
                    <Icon name="ic:baseline-calendar-month" />
                    Day
                    {{
                        faker.number.int({ min: 1, max: props.data.duration })
                    }}/{{ props.data.duration }}
                </p>
                <p class="text-sm flex items-center text-green-500 gap-1">
                    {{ (props.data as Program).progress }}%
                </p>
            </div>

            <div v-else class="flex items-center justify-between mt-auto">
                <p class="text-muted/90 text-sm flex items-center gap-1">
                    <Icon name="ic:outline-access-time" />
                    {{ props.data.duration }} days
                </p>
                <p class="text-sm flex items-center text-text gap-1">
                    {{ props.data?.rating }}/5
                    <Icon
                        name="material-symbols:star-rounded"
                        class="text-yellow-400 text-2xl"
                    />
                </p>
            </div>

            <progress
                v-if="isInProgress"
                class="progress progress-success w-full mt-4"
                :value="(props.data as Program).progress"
                max="100"
            ></progress>

            <AppButton
                v-if="isInProgress"
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
        </div>
    </article>
</template>
<script setup lang="ts">
import { faker } from "@faker-js/faker";
import type { Activity } from "~/models/activity.model";
import type { Program } from "~/models/program.model";

const props = defineProps<{
    data: Activity | Program;
}>();

const isProgram = typeof props.data;
const isInProgress = isProgram && (props.data as Program).progress != undefined;
</script>
