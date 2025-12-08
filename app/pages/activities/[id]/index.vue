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
                <div class="flex">
                    <h1 class="font-bold text-3xl mt-1 text-text">
                        {{ activity?.name }}
                    </h1>
                    <NuxtLink
                        :to="'/activities/' + route.params.id + '/edit'"
                        class="ml-auto"
                    >
                        <AppButton color="black" class="ml-auto px-4"
                            >Edit</AppButton
                        >
                    </NuxtLink>
                </div>
                <p class="mt-1 text-muted-foreground flex items-center">
                    <Icon class="" name="ic:outline-access-time" />
                    <span class="ml-1"
                        >{{ activity?.duration_minutes }} minutes</span
                    >
                </p>
            </div>
            <p class="text-text font-medium text-sm mt-3">Description</p>
            <p class="text-muted-foreground text-sm mb-4 mt-1">
                {{ activity?.description }}
            </p>

            <slot></slot>
        </div>
    </article>
</template>
<script setup lang="ts">
import type { Activity } from "~/models/activity.model";

const route = useRoute();

const { data: activity } = await useFetch<Activity>(
    `/api/activities/${route.params.id}`,
);
</script>
