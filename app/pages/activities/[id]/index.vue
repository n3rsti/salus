<template>
    <article
        class="flex flex-col border rounded-xl p-3 sm:p-5 md:p-6 lg:p-7 bg-primary-light border-neutral-100 border-t border-t-transparent shadow grow"
    >
        <img
            :src="'/media/' + activity?.image_url"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow p-2 mt-3">
            <div class="flex">
                <h1 class="font-bold text-3xl mt-1 text-text">
                    {{ activity?.name }}
                    <Badge
                        v-if="activity"
                        class="text-xs rounded-md"
                        :class="DifficultiesColors[activity?.difficulty]"
                        >{{ Difficulties[activity.difficulty] }}</Badge
                    >
                </h1>
                <NuxtLink
                    v-if="userStore.id == activity?.owner?.id"
                    :to="'/activities/' + route.params.id + '/edit'"
                    class="ml-auto"
                >
                    <Button variant="default" class="ml-auto px-4">Edit</Button>
                </NuxtLink>
            </div>
            <div class="flex mt-1">
                <p class="text-muted-foreground flex items-center">
                    <Icon class="" name="ic:outline-access-time" />
                    <span class="ml-1"
                        >{{ activity?.duration_minutes }} minutes</span
                    >
                </p>
                <p class="ml-auto">
                    by
                    <NuxtLink
                        class="font-semibold"
                        :to="'/users/' + activity?.owner?.username"
                    >
                        {{ activity?.owner?.username }}
                    </NuxtLink>
                </p>
            </div>
            <p class="text-text font-medium text-sm mt-3">Description</p>
            <p class="text-muted-foreground text-sm mb-4 mt-1">
                {{ activity?.description }}
            </p>

            <slot></slot>

            <Button variant="success" class="mt-auto">Start</Button>
        </div>
    </article>
</template>
<script setup lang="ts">
import { Badge } from "~/components/ui/badge";
import { Button } from "~/components/ui/button";
import { Difficulties, DifficultiesColors } from "~/constants/difficulty";
import type { Activity } from "~/models/activity.model";

const route = useRoute();
const userStore = useUserStore();

const { data: activity } = await useFetch<Activity>(
    `/api/activities/${route.params.id}`,
);
</script>
