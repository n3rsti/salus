<template>
    <article
        class="flex flex-col border rounded-xl p-3 bg-primary-light border-neutral-100 border-t border-t-primary shadow"
    >
        <img
            :src="faker.image.url()"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary_light border-t-transparent"
        />
        <div class="flex flex-col grow p-2">
            <h3 class="font-semibold color-text text-lg mt-1">
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
                <p class="text-sm flex items-center gap-1">
                    4.5/5
                    <Icon
                        name="material-symbols:star-rounded"
                        class="text-yellow-400 text-2xl"
                    />
                </p>
            </div>

            <AppButton
                class="w-full bg-green-500 border-green-300 shadow-green-500 text-white mt-4"
            >
                View info
            </AppButton>
        </div>
    </article>
</template>
<script setup lang="ts">
import { faker } from "@faker-js/faker";
import type { Activity } from "~/models/activity.model";

const model = defineModel<Activity>();
</script>
