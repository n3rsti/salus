<template>
    <article
        class="flex flex-col border rounded-xl p-3 bg-primary-light border-neutral-100 border-t border-t-transparent shadow"
    >
        <img
            :src="model?.image"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow p-2">
            <h3 class="font-semibold text-text text-lg mt-1">
                {{ model?.name }}
            </h3>
            <p class="text-muted text-sm mt-1">
                {{ model?.description }}
            </p>

            <div class="flex items-center justify-between mt-4">
                <p
                    v-if="model?.duration"
                    class="text-muted/90 text-sm flex items-center gap-1"
                >
                    <Icon name="ic:outline-access-time" />
                    {{ model.duration }} days
                </p>
                <p class="text-sm flex items-center text-text gap-1">
                    {{ model?.rating }}/5
                    <Icon
                        name="material-symbols:star-rounded"
                        class="text-yellow-400 text-2xl"
                    />
                </p>
            </div>

            <progress
                v-if="false"
                class="progress progress-success w-full mt-4"
                value="50"
                max="100"
            ></progress>

            <AppButton
                class="w-full shadow-sm border-t-transparent text-white mt-3"
                :color="'green'"
            >
                View info
            </AppButton>
        </div>
    </article>
</template>
<script setup lang="ts">
import type { Activity } from "~/models/activity.model";

const model = defineModel<Activity>();
</script>
