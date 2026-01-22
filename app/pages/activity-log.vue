<template>
    <div class="flex flex-col gap-4">
        <div
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">Activity log</h1>
        </div>
        <div v-for="section in dateSections" :key="section.key">
            <div class="text-sm font-semibold text-primary">
                {{ section.label }}
            </div>

            <div class="flex flex-col gap-2 mt-2">
                <div
                    v-for="group of section.items"
                    :key="
                        group.type + (group.program?.id || group.activity?.id)
                    "
                >
                    <div v-if="group.type === 'program' && group.program">
                        <article
                            class="collapse md:collapse-arrow grow-0 bg-card text-card-foreground border border-primary-dark rounded-xl shadow-sm"
                        >
                            <input type="checkbox" />
                            <div
                                class="flex items-center collapse-title max-md:px-2"
                            >
                                <NuxtLink
                                    :to="'/programs/' + group.program.id"
                                    class="z-10 relative hover:underline"
                                >
                                    <h2
                                        class="font-medium text-primary text-sm flex items-center"
                                    >
                                        {{ group.program.name }}
                                    </h2>
                                </NuxtLink>

                                <div
                                    v-if="group.stats"
                                    class="flex items-center ml-auto gap-3"
                                >
                                    <progress
                                        :value="
                                            (group.stats.completed /
                                                group.stats.total) *
                                            100
                                        "
                                        min="0"
                                        max="100"
                                        class="rounded-xl w-20 md:w-32 bg-gray-100 h-3 [&::-webkit-progress-value]:bg-green-500 [&::-moz-progress-bar]:bg-green-500"
                                    ></progress>
                                    <p class="text-sm">
                                        {{ group.stats.completed }} /
                                        {{ group.stats.total }}
                                    </p>
                                </div>
                            </div>

                            <div class="collapse-content">
                                <div
                                    v-for="day in group.program.days"
                                    :key="day.day_number"
                                    class="last:mb-6 md:last:mb-3 flex flex-col gap-2 not-first:mt-5"
                                >
                                    <div
                                        class="font-semibold text-primary text-sm"
                                    >
                                        Day {{ day.day_number }}
                                    </div>

                                    <NuxtLink
                                        v-for="activity in day.activities"
                                        :key="activity.id"
                                        :to="
                                            '/activities/' +
                                            activity.id +
                                            '?program=' +
                                            group.program.id +
                                            '&day=' +
                                            day.id
                                        "
                                        class="first:mt-2"
                                    >
                                        <AppVerticalCard
                                            :img="activity.image_url"
                                        >
                                            <template #name>
                                                {{ activity.name }}
                                            </template>

                                            <template #badge>
                                                <Badge
                                                    v-if="
                                                        badgeMeta(
                                                            getUserActivityFromProgram(
                                                                group.program,
                                                                activity.id!,
                                                            ),
                                                        )
                                                    "
                                                    class="text-xs rounded-md px-1 py-0.5"
                                                    :class="
                                                        badgeMeta(
                                                            getUserActivityFromProgram(
                                                                group.program,
                                                                activity.id!,
                                                            ),
                                                        )!.color
                                                    "
                                                >
                                                    {{
                                                        badgeMeta(
                                                            getUserActivityFromProgram(
                                                                group.program,
                                                                activity.id!,
                                                            ),
                                                        )!.label
                                                    }}
                                                </Badge>
                                            </template>

                                            <template #description>
                                                {{ activity.description }}
                                            </template>
                                        </AppVerticalCard>
                                    </NuxtLink>
                                </div>
                            </div>
                        </article>
                    </div>

                    <div v-else-if="group.type === 'standalone'">
                        <NuxtLink
                            v-if="group.activity?.activity"
                            :to="'/activities/' + group.activity.activity.id"
                        >
                            <AppVerticalCard
                                :img="group.activity.activity.image_url"
                            >
                                <template #name>
                                    {{ group.activity.activity.name }}
                                </template>

                                <template #badge>
                                    <Badge
                                        v-if="badgeMeta(group.activity)"
                                        class="text-xs rounded-md px-1 py-0.5"
                                        :class="
                                            badgeMeta(group.activity)!.color
                                        "
                                    >
                                        {{ badgeMeta(group.activity)!.label }}
                                    </Badge>
                                </template>

                                <template #description>
                                    {{ group.activity.activity.description }}
                                </template>
                            </AppVerticalCard>
                        </NuxtLink>
                    </div>
                </div>
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
import type {
    UserActivitiesResponse,
    UserActivity,
    ProgramWithActivities,
} from "~/models/user_activities_response.model";

const { $api } = useNuxtApp();

const { data } = await useFetch<UserActivitiesResponse>(
    "/api/user-activities/me/activities?limit=50",
    { method: "GET", $fetch: $api },
);

const activities = computed(() => data.value?.activities ?? []);

const programsById = computed(() => {
    const map = new Map<number, ProgramWithActivities>();
    for (const p of data.value?.programs ?? []) map.set(p.id, p);
    return map;
});

const activitiesById = computed(() => {
    const map = new Map<number, UserActivity>();
    for (const a of activities.value) map.set(a.id, a);
    return map;
});

interface RenderGroup {
    type: "program" | "standalone";
    program?: ProgramWithActivities;
    activity?: UserActivity;
    newestDate: Date;
    stats?: {
        completed: number;
        inProgress: number;
        notStarted: number;
        total: number;
    };
}

const renderGroups = computed<RenderGroup[]>(() => {
    if (!data.value) return [];

    const programActivitiesByProgramId = new Map<number, UserActivity[]>();
    const standalone: RenderGroup[] = [];

    for (const ua of activities.value) {
        if (ua.program_id) {
            const list = programActivitiesByProgramId.get(ua.program_id) ?? [];
            list.push(ua);
            programActivitiesByProgramId.set(ua.program_id, list);
            continue;
        }

        if (ua.program_id === null && ua.activity !== null) {
            standalone.push({
                type: "standalone",
                activity: ua,
                newestDate: new Date(ua.start_date),
            });
        }
    }

    const programGroups: RenderGroup[] = [];
    for (const [programId, programActivities] of programActivitiesByProgramId) {
        const program = programsById.value.get(programId);

        const newest = programActivities.reduce((best, cur) =>
            new Date(cur.start_date) > new Date(best.start_date) ? cur : best,
        );

        const completed = programActivities.filter(
            (a) => a.end_date !== null,
        ).length;
        const inProgress = programActivities.filter(
            (a) => a.end_date === null && a.activity !== null,
        ).length;

        const total =
            program?.days.reduce(
                (sum, day) => sum + day.activities.length,
                0,
            ) ?? 0;

        const notStarted = total - completed - inProgress;

        programGroups.push({
            type: "program",
            program,
            newestDate: new Date(newest.start_date),
            stats: { completed, inProgress, notStarted, total },
        });
    }

    return [...programGroups, ...standalone].sort(
        (a, b) => b.newestDate.getTime() - a.newestDate.getTime(),
    );
});

const formatDate = (date: string | Date) => {
    return new Date(date).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
    });
};

function dateKey(d: Date) {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(
        d.getDate(),
    ).padStart(2, "0")}`;
}

const dateSections = computed(() => {
    const sections: { key: string; label: string; items: RenderGroup[] }[] = [];

    for (const item of renderGroups.value) {
        const key = dateKey(item.newestDate);
        const last = sections[sections.length - 1];

        if (!last || last.key !== key) {
            sections.push({
                key,
                label: formatDate(item.newestDate),
                items: [item],
            });
        } else {
            last.items.push(item);
        }
    }

    return sections;
});

function getStatus(activity: UserActivity | undefined): ActivityStatus {
    if (!activity) return ActivityStatus.NotStarted;
    if (activity.end_date) return ActivityStatus.Completed;
    return ActivityStatus.InProgress;
}

function badgeMeta(activity: UserActivity | undefined) {
    const status = getStatus(activity);
    if (status === ActivityStatus.NotStarted) return null;

    return {
        status,
        label: ActivityStatusNames[status],
        color: ActivityStatusColors[status],
    };
}

function getUserActivityFromProgram(
    program: ProgramWithActivities,
    activityId: number,
): UserActivity | undefined {
    const userActivityId = program.user_activities[activityId];
    if (!userActivityId) return undefined;
    return activitiesById.value.get(userActivityId);
}
</script>
