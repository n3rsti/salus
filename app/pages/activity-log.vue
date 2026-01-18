<template>
    <div>
        <div
            v-for="group of renderGroups"
            v-bind:key="group.type + (group.program?.id || group.activity?.id)"
        >
            <div v-if="group.type == 'program'">
                <div class="grid grid-cols-1 gap-2 items-start">
                    <div
                        v-for="day in group.program?.days"
                        :key="day.day_number"
                        class="rounded-xl border-primary-dark border collapse collapse-arrow last:mb-6 md:last:mb-3"
                    >
                        <input type="checkbox" :checked="day.day_number == 1" />
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
                                :to="
                                    '/activities/' +
                                    activity.id +
                                    '?programId=' +
                                    group.program?.id
                                "
                            >
                                <AppVerticalCard :img="activity.image_url">
                                    <template #name>
                                        {{ activity.name }}
                                    </template>
                                    <template #badge>
                                        <Badge
                                            v-if="
                                                getStatus(
                                                    activity.id,
                                                    day.id,
                                                ) !== ActivityStatus.NotStarted
                                            "
                                            class="text-xs rounded-md px-1 py-0.5"
                                            :class="
                                                ActivityStatusColors[
                                                    getStatus(
                                                        activity.id,
                                                        day.id,
                                                    )
                                                ]
                                            "
                                            >{{
                                                ActivityStatusNames[
                                                    getStatus(
                                                        activity.id,
                                                        day.id,
                                                    )
                                                ]
                                            }}</Badge
                                        >
                                    </template>
                                    <template #description>
                                        {{ activity.description }}
                                    </template>
                                </AppVerticalCard>
                            </NuxtLink>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else>
                <NuxtLink
                    v-if="group.activity?.activity"
                    :to="'/activities/' + group.activity.activity.id"
                >
                    <AppVerticalCard :img="group.activity.activity.image_url">
                        <template #name>
                            {{ group.activity.activity.name }}
                        </template>
                        <template #badge>
                            <Badge
                                v-if="
                                    getStatus(
                                        group.activity.activity.id,
                                        null,
                                    ) !== ActivityStatus.NotStarted
                                "
                                class="text-xs rounded-md px-1 py-0.5"
                                :class="
                                    ActivityStatusColors[
                                        getStatus(
                                            group.activity.activity.id,
                                            null,
                                        )
                                    ]
                                "
                                >{{
                                    ActivityStatusNames[
                                        getStatus(
                                            group.activity.activity.id,
                                            null,
                                        )
                                    ]
                                }}</Badge
                            >
                        </template>
                        <template #description>
                            {{ group.activity.activity.description }}
                        </template>
                    </AppVerticalCard>
                </NuxtLink>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Badge } from "~/components/ui/badge";
import {
    ActivityStatus,
    ActivityStatusColors,
    ActivityStatusNames,
} from "~/constants/activity_status";
import { Difficulties, DifficultiesColors } from "~/constants/difficulty";
import type { Activity } from "~/models/activity.model";
import type {
    UserActivitiesResponse,
    UserActivity,
    ProgramWithActivities,
} from "~/models/user_activities_response.model";

interface ActivityGroup {
    type: "program" | "standalone";
    programId?: number;
    program?: ProgramWithActivities;
    activities: UserActivity[];
    programStartActivity?: UserActivity; // The "program start" entry
}

const { data } = await useFetch<UserActivitiesResponse>(
    "/api/user-activities/me/activities?limit=50",
    {
        method: "GET",
    },
);

interface renderGroup {
    program?: ProgramWithActivities;
    activity?: UserActivity;
}

console.log(data.value);

interface RenderGroup {
    type: "program" | "standalone";
    program?: ProgramWithActivities;
    activity?: UserActivity;
    newestDate: Date;
}

const renderGroups = computed<RenderGroup[]>(() => {
    if (!data.value) return [];
    const groups: RenderGroup[] = [];
    const seenPrograms = new Set<number>();

    for (const activity of data.value?.activities ?? []) {
        if (activity.program_id) {
            if (!seenPrograms.has(activity.program_id)) {
                seenPrograms.add(activity.program_id);

                const programActivities = data.value.activities.filter(
                    (a) => a.program_id === activity.program_id,
                );

                const newestActivity = programActivities.reduce(
                    (newest, current) =>
                        new Date(current.start_date) >
                        new Date(newest.start_date)
                            ? current
                            : newest,
                    activity,
                );

                groups.push({
                    type: "program",
                    program: data.value?.programs.find(
                        (p) => p.id === activity.program_id,
                    ),
                    newestDate: new Date(newestActivity.start_date),
                });
            }
        } else if (activity.program_id === null && activity.activity !== null) {
            groups.push({
                type: "standalone",
                activity: activity,
                newestDate: new Date(activity.start_date),
            });
        }
    }
    console.log(groups);

    return groups.sort(
        (a, b) => b.newestDate.getTime() - a.newestDate.getTime(),
    );
});

console.log(renderGroups.value);

const formatDate = (date: string | Date) => {
    return new Date(date).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
    });
};

function getStatus(
    activityId: number | undefined,
    dayNumber: number | undefined | null,
): ActivityStatus {
    const activity = data.value?.activities.find(
        (a) => a.activity?.id === activityId && a.program_day_id === dayNumber,
    );
    if (!activity) return ActivityStatus.NotStarted;
    if (activity.end_date) return ActivityStatus.Completed;
    return ActivityStatus.InProgress;
}
</script>
