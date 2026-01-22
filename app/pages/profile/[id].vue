<script setup lang="ts">
import { Skeleton } from "~/components/ui/skeleton";
import type { Activity } from "~/models/activity.model";
import type { Program } from "~/models/program.model";
import type { User } from "~/models/user.model";

definePageMeta({
    public: true,
});

const route = useRoute();
const user_id = route.params.id;

const { data: user } = useFetch<User>(`/api/users/${user_id}`);

const { data: programs } = useFetch<Program[]>(
    `/api/programs?user_id=${user_id}`,
);
const { data: activities } = useFetch<Activity[]>(
    `/api/activities?user_id=${user_id}&light=true`,
);
</script>

<template>
    <div class="flex flex-col gap-3">
        <div
            class="p-4 rounded-xl bg-primary-light flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">
                {{ user?.username }}
            </h1>
        </div>

        <div>
            <Card class="p-6">
                <h2 class="text-lg font-semibold mb-2">
                    Created programs
                    <span v-if="programs" class="text-sm text-muted-foreground"
                        >({{ programs?.length }})</span
                    >
                </h2>

                <div
                    v-if="!programs"
                    class="flex flex-col rounded-md py-2 px-2 gap-2"
                >
                    <div class="flex items-center gap-2">
                        <Skeleton class="h-8 aspect-square rounded-lg" />
                        <Skeleton class="w-20 h-4 rounded-md" />
                        <Skeleton class="w-12 h-5 rounded-md" />
                        <Skeleton class="ml-auto w-20 h-5 rounded-md" />
                    </div>
                    <Skeleton class="w-full h-5 rounded-md" />
                </div>

                <p v-if="programs?.length == 0" class="text-gray-500">
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
                                {{ program.name }}
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
                <h2 class="text-lg font-semibold mb-2">
                    Created activities
                    <span
                        v-if="activities"
                        class="text-sm text-muted-foreground"
                        >({{ activities?.length }})</span
                    >
                </h2>

                <div
                    v-if="!activities"
                    class="flex flex-col rounded-md py-2 px-2 gap-2"
                >
                    <div class="flex items-center gap-2">
                        <Skeleton class="h-8 aspect-square rounded-lg" />
                        <Skeleton class="w-20 h-4 rounded-md" />
                        <Skeleton class="w-12 h-5 rounded-md" />
                        <Skeleton class="ml-auto w-20 h-5 rounded-md" />
                    </div>
                    <Skeleton class="w-full h-5 rounded-md" />
                </div>

                <p v-if="activities?.length == 0" class="text-gray-500">
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
