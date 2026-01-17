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
                                        {{ activity.id }}
                                        {{ getStatus(activity.id) }}
                                    </p>

                                    <Badge
                                        class="text-xs rounded-md px-1 py-0.5"
                                        :class="
                                            DifficultiesColors[
                                                activity.difficulty
                                            ]
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
            </div>
            <div v-else>Activity</div>
        </div>
    </div>
</template>

<script setup lang="ts">
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

console.log(data.value?.activities);

interface RenderGroup {
    type: "program" | "standalone";
    program?: ProgramWithActivities;
    activity?: UserActivity;
    newestDate: Date;
}

const renderGroups = computed<RenderGroup[]>(() => {
    if (!data.value) return [];
    const groups: RenderGroup[] = [];
    const seenProgramStarts = new Set<number>();

    for (const activity of data.value?.activities ?? []) {
        if (activity.program_id && !activity.activity) {
            if (!seenProgramStarts.has(activity.id)) {
                seenProgramStarts.add(activity.id);

                const programActivities = data.value.activities.filter(
                    (a) =>
                        a.program_id === activity.program_id &&
                        new Date(a.start_date) >= new Date(activity.start_date),
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
        } else if (!activity.program_id && activity.activity) {
            groups.push({
                type: "standalone",
                activity: activity,
                newestDate: new Date(activity.start_date),
            });
        }
    }

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

function getStatus(activityId: number | undefined): string {
    const activity = data.value?.activities.find(
        (a) => a.activity?.id === activityId,
    );
    if (!activity) return "not_started";
    if (activity.end_date) return "completed";
    return "in_progress";
}
</script>
