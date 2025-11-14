<template>
    <article
        class="flex flex-col border rounded-xl p-3 sm:p-5 md:p-6 lg:p-7 bg-primary-light border-neutral-100 border-t border-t-transparent shadow grow"
    >
        <img
            :src="program?.image_url"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow p-2 mt-3">
            <div class="flex items-end">
                <h1 class="font-bold text-3xl text-text mt-1">
                    {{ program?.name }}
                </h1>
                <p class="ml-3 text-muted flex items-center">
                    <Icon class="" name="ic:outline-access-time" />
                    <span class="ml-1">{{ program?.duration_days }} days</span>
                </p>
            </div>
            <p class="text-muted text-sm mt-2 mb-4">
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
                        Day {{ day.day_number + 1 }}
                    </div>
                    <div class="px-2 collapse-content">
                        <p class="text-sm text-muted px-2 mb-3">
                            {{ day.description }}
                        </p>
                        <div
                            v-for="activity in day.activities"
                            :key="activity.id"
                            class="flex flex-col w-full gap-2 p-3 border border-primary-dark rounded-xl mt-2"
                        >
                            <div class="flex items-center w-full">
                                <img
                                    :src="activity.image_url"
                                    alt=""
                                    class="h-8 aspect-square rounded-lg"
                                />
                                <p class="text-text font-medium text-sm ml-2">
                                    {{ activity.name }}
                                </p>

                                <NuxtLink
                                    :to="'/activities/' + activity.id"
                                    class="ml-auto"
                                >
                                    <AppButton
                                        class="w-full shadow-sm border-t-transparent text-white ml-auto"
                                        :color="'green_dark'"
                                    >
                                        View info
                                        <Icon
                                            class="text-lg ml-2"
                                            name="ic:round-remove-red-eye"
                                        />
                                    </AppButton>
                                </NuxtLink>
                            </div>
                            <div class="w-full">
                                <p class="text-muted/80 text-xs">
                                    {{ activity.description }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <slot></slot>
        </div>
    </article>
</template>
<script setup lang="ts">
import type { Program } from "~/models/program.model";

const config = useRuntimeConfig();
const route = useRoute();

const { data: program } = useFetch<Program>(`/api/programs/${route.params.id}`);
console.log(program);
</script>
