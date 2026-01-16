<template>
    <article
        class="flex flex-col border rounded-xl p-0 bg-transparent shadow-none sm:p-5 md:p-6 lg:p-7 md:bg-primary-light border-neutral-100 border-t border-t-transparent md:shadow grow"
    >
        <img
            :src="'/media/' + program?.image_url"
            alt=""
            class="object-cover w-full h-80 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow p-2 mt-3">
            <div class="flex mt-1">
                <h1 class="font-bold text-3xl text-text">
                    {{ program?.name }}
                </h1>
                <NuxtLink
                    v-if="userStore.id == program?.owner?.id"
                    :to="'/programs/' + route.params.id + '/edit'"
                    class="ml-auto"
                >
                    <Button variant="default" class="ml-auto px-4">Edit</Button>
                </NuxtLink>
            </div>

            <div class="flex gap-8">
                <section>
                    <p class="text-text font-medium text-sm mt-3">Duration</p>
                    <div class="flex">
                        <p class="text-muted-foreground flex items-center">
                            <Icon class="" name="ic:outline-access-time" />
                            <span class="ml-1 text-sm"
                                >{{ program?.duration_days }} days</span
                            >
                        </p>
                    </div>
                </section>
                <section>
                    <p class="text-text font-medium text-sm mt-3">Author</p>
                    <NuxtLink
                        class="font-semibold text-sm"
                        :to="'/users/' + program?.owner?.username"
                    >
                        {{ program?.owner?.username }}
                    </NuxtLink>
                </section>
            </div>

            <p class="text-text font-medium text-sm mt-3">Tags</p>
            <section class="flex gap-1 flex-wrap my-2">
                <Badge
                    v-for="tag in program?.tags"
                    :key="tag"
                    class="text-xs rounded-md p-0.5 px-1 text-center shadow-xs font-semibold"
                    :class="TagColors[tag]"
                >
                    <Icon :name="TagIcons[tag]" />
                    {{ TagNames[tag] }}</Badge
                >
            </section>

            <p class="text-text font-medium text-sm mt-3">Description</p>
            <p class="text-muted-foreground text-sm mb-4 mt-1">
                {{ program?.description }}
            </p>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-2 items-start">
                <div
                    v-for="day in program?.days"
                    :key="day.day_number"
                    class="rounded-xl border-primary-dark border collapse collapse-arrow last:mb-3"
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
                            <div class="flex items-center w-full gap-2">
                                <img
                                    :src="'/media/' + activity.image_url"
                                    alt=""
                                    class="h-8 aspect-square rounded-lg"
                                />
                                <p
                                    class="text-text font-medium text-sm hover:underline py-1"
                                >
                                    {{ activity.name }}
                                </p>

                                <Badge
                                    class="text-xs rounded-md px-1 py-0.5"
                                    :class="
                                        DifficultiesColors[activity.difficulty]
                                    "
                                    >{{
                                        Difficulties[activity.difficulty]
                                    }}</Badge
                                >
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
import Badge from "~/components/ui/badge/Badge.vue";
import { Button } from "~/components/ui/button";
import { Difficulties, DifficultiesColors } from "~/constants/difficulty";
import { TagColors, TagIcons, TagNames } from "~/constants/tags";
import type { Program } from "~/models/program.model";

const route = useRoute();
const userStore = useUserStore();

const { data: program } = await useFetch<Program>(
    `/api/programs/${route.params.id}`,
);
</script>
