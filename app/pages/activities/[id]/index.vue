<template>
    <article
        class="flex flex-col border rounded-xl p-3 sm:p-5 md:p-6 lg:p-7 bg-primary-light border-neutral-100 border-t border-t-transparent shadow grow"
    >
        <img
            :src="'/media/' + activity?.image_url"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow p-2 mt-3">
            <div class="flex">
                <h1 class="font-bold text-3xl mt-1 text-text">
                    {{ activity?.name }}
                    <Badge
                        v-if="activity"
                        class="text-xs rounded-md"
                        :class="DifficultiesColors[activity?.difficulty]"
                        >{{ Difficulties[activity.difficulty] }}</Badge
                    >
                </h1>
                <NuxtLink
                    v-if="userStore.id == activity?.owner?.id"
                    :to="'/activities/' + route.params.id + '/edit'"
                    class="ml-auto"
                >
                    <Button variant="default" class="ml-auto px-4">Edit</Button>
                </NuxtLink>
            </div>
            <div class="flex mt-1">
                <p class="text-muted-foreground flex items-center">
                    <Icon class="" name="ic:outline-access-time" />
                    <span class="ml-1"
                        >{{ activity?.duration_minutes }} minutes</span
                    >
                </p>
                <p class="ml-auto">
                    by
                    <NuxtLink
                        class="font-semibold"
                        :to="'/users/' + activity?.owner?.username"
                    >
                        {{ activity?.owner?.username }}
                    </NuxtLink>
                </p>
            </div>
            <p class="text-text font-medium text-sm mt-3">Description</p>
            <p class="text-muted-foreground text-sm mb-4 mt-1">
                {{ activity?.description }}
            </p>

            <slot></slot>

            <Dialog v-if="!isStarted">
                <DialogTrigger class="mt-auto">
                    <Button variant="success" class="mt-auto w-full"
                        >Start</Button
                    >
                </DialogTrigger>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Start activity</DialogTitle>
                        <DialogDescription>
                            Do you want to start this activity?
                        </DialogDescription>
                    </DialogHeader>
                    <DialogFooter>
                        <Button variant="success" @click="startActivity"
                            >Start</Button
                        >
                    </DialogFooter>
                </DialogContent>
            </Dialog>
            <section
                v-else
                class="grid grid-cols-1 md:grid-cols-[2fr_1fr] gap-1 w-full mt-auto"
            >
                <Dialog>
                    <DialogTrigger>
                        <Button variant="success" class="w-full"
                            >Mark completed <span class="ml-1">🎉</span></Button
                        >
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Congratulations 🎉</DialogTitle>
                            <DialogDescription>
                                Do you want to mark this activity as completed?
                            </DialogDescription>
                        </DialogHeader>
                        <DialogFooter>
                            <Button variant="success" @click="completeActivity"
                                >Complete</Button
                            >
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
                <Dialog>
                    <DialogTrigger>
                        <Button variant="destructive" class="w-full"
                            >Cancel</Button
                        >
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Cancel activity</DialogTitle>
                            <DialogDescription>
                                Do you want to cancel this activity?
                            </DialogDescription>
                        </DialogHeader>
                        <DialogFooter>
                            <Button
                                variant="destructive"
                                @click="cancelActivity"
                                >Cancel</Button
                            >
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </section>
        </div>
    </article>
</template>
<script setup lang="ts">
import { Badge } from "~/components/ui/badge";
import { Button } from "~/components/ui/button";
import {
    Dialog,
    DialogFooter,
    DialogHeader,
    DialogContent,
    DialogDescription,
    DialogTitle,
    DialogTrigger,
} from "~/components/ui/dialog";
import { Difficulties, DifficultiesColors } from "~/constants/difficulty";
import type { Activity } from "~/models/activity.model";
import type { UserActivity } from "~/models/user_activity.model";

const route = useRoute();
const program = useRoute().query.program;
const userStore = useUserStore();
const { $api } = useNuxtApp();

const { data: activity } = await useFetch<Activity>(
    `/api/activities/${route.params.id}`,
);

const { data: activity_log } =
    await useFetch<UserActivity[]>(`/api/user-activities`);

const startedActivity = computed(() => {
    console.log(activity_log.value);
    if (program) {
        return activity_log.value?.find(
            (log) =>
                log.activity_id === activity.value?.id &&
                log.end_date === null &&
                log.program_id == Number(program),
        );
    }
    return activity_log.value?.find(
        (log) =>
            log.activity_id === activity.value?.id && log.end_date === null,
    );
});
const isStarted = computed(() => {
    return startedActivity.value !== undefined;
});

async function completeActivity() {
    try {
        await $api(
            `/api/user-activities/${startedActivity.value?.id}/complete`,
            {
                method: "POST",
            },
        );
        activity_log.value = activity_log.value?.filter(
            (log) => log.id !== startedActivity.value?.id,
        );
    } catch (err) {
        console.error("Error completing activity:", err);
    }
}

async function startActivity() {
    try {
        const newActivity = await $api<UserActivity>(`/api/user-activities`, {
            method: "POST",
            body: {
                activity_id: activity.value?.id,
            },
        });

        activity_log.value = [...(activity_log.value || []), newActivity];
    } catch (err) {
        console.error("Error starting activity:", err);
    }
}

async function cancelActivity() {
    try {
        await $api(`/api/user-activities/${startedActivity.value?.id}`, {
            method: "DELETE",
        });
        activity_log.value = activity_log.value?.filter(
            (log) => log.id !== startedActivity.value?.id,
        );
    } catch (err) {
        console.error("Error cancelling activity:", err);
    }
}
</script>
