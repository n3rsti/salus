<script setup lang="ts">
import type { Activity } from "~/models/activity.model";
import type { Program } from "~/models/program.model";

definePageMeta({
    public: true,
});

const route = useRoute();
const user_id = route.params.id;

const { data: programs } = await useFetch<Program[]>(
    `/api/programs?user_id=${user_id}`,
);
const { data: activities } = await useFetch<Activity[]>(
    `/api/activities?user_id=${user_id}`,
);

const username = computed(() => {
    return activities.value?.[0]?.owner?.username;
});
</script>

<template>
    <div class="flex flex-col gap-3">
        <div
            class="p-4 rounded-xl bg-primary-light flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">{{ username }}</h1>
        </div>

        <div>
            <Card class="p-6">
                <h2 class="text-lg font-semibold mb-2">Created programs</h2>

                <p v-if="!programs?.length" class="text-gray-500">
                    No programs yet.
                </p>

                <section class="flex flex-col gap-2">
                    <NuxtLink
                        v-for="program in programs"
                        :key="program.id"
                        :to="'/programs/' + program.id"
                        class="first:mt-2"
                    >
                        <AppVerticalCard :img="program.image_url">
                            <template #name>
                                {{ program.name }} {{ program.owner?.username }}
                            </template>
                            <template #badge>
                                <template v-if="program.average_rating">
                                    <Icon
                                        name="material-symbols:star-rounded"
                                        class="text-yellow-400 text-xl"
                                    />
                                    <p class="text-xs font-medium">
                                        {{ program.average_rating.toFixed(1) }}
                                    </p>
                                </template>
                            </template>

                            <template #description>
                                {{ program.description }}
                            </template>
                        </AppVerticalCard>
                    </NuxtLink>
                </section>
            </Card>

            <Card class="p-6">
                <h2 class="text-lg font-semibold mb-2">Created activities</h2>

                <p v-if="!activities?.length" class="text-gray-500">
                    No activities yet.
                </p>

                <section class="flex flex-col gap-2">
                    <NuxtLink
                        v-for="activity in activities"
                        :key="activity.id"
                        :to="'/activities/' + activity.id"
                        class="first:mt-2"
                    >
                        <AppVerticalCard :img="activity.image_url">
                            <template #name>
                                {{ activity.name }}
                            </template>

                            <template #badge>
                                <template v-if="activity.average_rating">
                                    <Icon
                                        name="material-symbols:star-rounded"
                                        class="text-yellow-400 text-xl"
                                    />
                                    <p class="text-xs font-medium">
                                        {{ activity.average_rating.toFixed(1) }}
                                    </p>
                                </template>
                            </template>

                            <template #description>
                                {{ activity.description }}
                            </template>
                        </AppVerticalCard>
                    </NuxtLink>
                </section>
            </Card>
        </div>
    </div>
</template>
