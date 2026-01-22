<template>
    <div>
        <Card class="p-4 mb-4">
            <h2 class="text-green-700 text-xl">
                Good evening,
                <span class="text-green-800 font-semibold">{{
                    store.username
                }}</span
                >! 👋
            </h2>
        </Card>
        <section
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3 mb-8"
        >
            <AppMoodCard class="col-span-full"></AppMoodCard>

            <div
                class="flex items-center justify-between col-span-full mb-1 mt-6"
            >
                <h2 class="font-semibold text-xl flex">Programs</h2>
                <NuxtLink to="/programs/" class="ml-auto">
                    <Button variant="default">See more</Button>
                </NuxtLink>
            </div>
            <AppProgramCard
                v-for="program in programs"
                :key="program.id"
                :program="program"
            />

            <div
                class="flex items-center justify-between col-span-full mb-1 mt-10"
            >
                <h2 class="font-semibold text-xl flex">Activities</h2>
                <NuxtLink to="/activities/" class="ml-auto">
                    <Button variant="default">See more</Button>
                </NuxtLink>
            </div>
            <AppActivityCard
                v-for="activity in activities"
                :key="activity.id"
                :activity="activity"
            />
        </section>
    </div>
</template>
<script setup lang="ts">
import { Button } from "~/components/ui/button";
import { Card } from "~/components/ui/card";
import type { Activity } from "~/models/activity.model";
import type { Program } from "~/models/program.model";

const { $api } = useNuxtApp();

const limit = 10;
const { data: activities } = await useFetch<Activity[]>(
    `/api/activities?limit=${limit}&light=true`,
    {
        $fetch: $api,
    },
);

const { data: programs } = await useFetch<Program[]>(
    `/api/programs?limit=${limit}&light=true`,
);

const store = useUserStore();
</script>
