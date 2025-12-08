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
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3"
        >
            <AppMoodCard class="lg:col-span-2"></AppMoodCard>

            <AppProgramCard
                v-for="program in programs"
                :key="program.id"
                :program="program"
            />
            <AppActivityCard
                v-for="activity in activities"
                :key="activity.id"
                :activity="activity"
            />
        </section>
    </div>
</template>
<script setup lang="ts">
import { Card } from "~/components/ui/card";
import type { Activity } from "~/models/activity.model";
import type { Program } from "~/models/program.model";

const { data: activities } = await useFetch<Activity[]>(`/api/activities`);

const { data: programs } = await useFetch<Program[]>(`/api/programs`);

const store = useUserStore();
</script>
