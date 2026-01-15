<template>
    <article
        class="flex flex-col border rounded-xl p-3 sm:p-5 md:p-6 lg:p-7 bg-primary-light border-neutral-100 border-t border-t-transparent shadow grow"
    >
        <img
            :src="'/media/' + program?.image_url"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow p-2 mt-3">
            <div>
                <div class="flex mt-1">
                    <h1 class="font-bold text-3xl text-text">
                        {{ program?.name }}
                    </h1>
                    <NuxtLink
                        v-if="userStore.id == program?.owner?.id"
                        :to="'/programs/' + route.params.id + '/edit'"
                        class="ml-auto"
                    >
                        <Button variant="default" class="ml-auto px-4"
                            >Edit</Button
                        >
                    </NuxtLink>
                </div>
                <div class="flex mt-1">
                    <p class="text-muted-foreground flex items-center">
                        <Icon class="" name="ic:outline-access-time" />
                        <span class="ml-1"
                            >{{ program?.duration_days }} days</span
                        >
                    </p>
                    <p class="ml-auto">
                        by
                        <NuxtLink
                            class="font-semibold"
                            :to="'/users/' + program?.owner?.username"
                        >
                            {{ program?.owner?.username }}
                        </NuxtLink>
                    </p>
                </div>
            </div>
            <p class="text-text font-medium text-sm mt-3">Description</p>
            <p class="text-muted-foreground text-sm mb-4 mt-1">
                {{ program?.description }}
            </p>

            <div class="flex flex-col gap-2">
                <div
                    v-for="day in program?.days"
                    :key="day.day_number"
                    class="rounded-xl border-primary-dark border collapse collapse-arrow"
                >
                    <input type="checkbox" checked />
                    <div class="collapse-title font-semibold text-text">
                        Day {{ day.day_number }}
                    </div>
                    <div class="px-2 collapse-content">
                        <p class="text-sm text-muted-foreground px-2 mb-3">
                            {{ day.description }}
                        </p>
                        <NuxtLink
                            v-for="activity in day.activities"
                            :key="activity.id"
                            :to="'/activities/' + activity.id"
                            class="flex flex-col w-full gap-2 p-3 border border-primary-dark rounded-xl mt-2 hover:outline"
                        >
                            <div class="flex items-center w-full">
                                <img
                                    :src="'/media/' + activity.image_url"
                                    alt=""
                                    class="h-8 aspect-square rounded-lg"
                                />
                                <p
                                    class="text-text font-medium text-sm ml-2 hover:underline py-1"
                                >
                                    {{ activity.name }}
                                </p>
                            </div>
                            <div class="w-full">
                                <p class="text-muted-foreground text-xs">
                                    {{ activity.description }}
                                </p>
                            </div>
                        </NuxtLink>
                    </div>
                </div>
            </div>

            <slot></slot>
            <Button variant="success" class="mt-auto">Start</Button>
        </div>
    </article>
</template>
<script setup lang="ts">
import { Button } from "~/components/ui/button";
import type { Program } from "~/models/program.model";

const route = useRoute();
const userStore = useUserStore();

const { data: program } = await useFetch<Program>(
    `/api/programs/${route.params.id}`,
);
</script>
