<template>
    <div>
        <Card class="p-4 mb-4 flex-row items-center">
            <h1 class="text-green-700 text-xl font-semibold">Activities</h1>
            <NuxtLink to="/activities/create" class="ml-auto">
                <Button variant="success">Create</Button>
            </NuxtLink>
        </Card>

        <section
            class="w-full grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3"
        >
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

const { data: activities } = await useFetch<Activity[]>(
    `/api/activities?light=true`,
);
</script>
