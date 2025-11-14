<template>
    <article
        class="flex flex-col border rounded-xl p-3 sm:p-5 md:p-6 lg:p-7 bg-primary-light border-neutral-100 border-t border-t-transparent shadow grow"
    >
        <img
            :src="activity?.image_url"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow p-2 mt-3">
            <div>
                <h1 class="font-bold text-3xl mt-1 text-text">
                    {{ activity?.name }}
                </h1>
                <p class="mt-1 text-muted flex items-center">
                    <Icon class="" name="ic:outline-access-time" />
                    <span class="ml-1"
                        >{{ activity?.duration_minutes }} minutes</span
                    >
                </p>
            </div>
            <p class="text-text font-medium text-sm mt-3">Description</p>
            <p class="text-muted text-sm mb-4 mt-1">
                {{ activity?.description }}
            </p>

            <slot></slot>
        </div>
    </article>
</template>
<script setup lang="ts">
import type { Activity } from "~/models/activity.model";

const route = useRoute();
const config = useRuntimeConfig();

const { data: activity } = await useFetch<Activity>(
    `/api/activities/${route.params.id}`,
);
</script>
