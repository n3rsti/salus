<template>
    <article
        class="flex flex-col border rounded-xl p-0 bg-transparent shadow-none sm:p-5 md:p-6 lg:p-7 md:bg-primary-light border-neutral-100 border-t border-t-transparent md:shadow grow"
    >
        <img
            :src="'/media/' + program?.image_url"
            alt=""
            class="object-cover w-full h-80 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <section class="flex flex-col grow p-2 mt-3 relative gap-3">
            <section class="flex">
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
            </section>

            <section class="flex gap-8">
                <section>
                    <p class="text-text font-medium text-sm">Duration</p>
                    <p class="text-muted-foreground flex items-center">
                        <Icon class="" name="ic:outline-access-time" />
                        <span class="ml-1 text-sm"
                            >{{ program?.duration_days }} days</span
                        >
                    </p>
                </section>
                <section>
                    <p class="text-text font-medium text-sm">Author</p>
                    <NuxtLink
                        class="font-semibold text-sm"
                        :to="'/users/' + program?.owner?.username"
                    >
                        {{ program?.owner?.username }}
                    </NuxtLink>
                </section>
            </section>

            <section>
                <p class="text-text font-medium text-sm">Tags</p>
                <div class="flex gap-1 flex-wrap my-2">
                    <Badge
                        v-for="tag in program?.tags"
                        :key="tag"
                        class="text-xs rounded-md p-0.5 px-1 text-center shadow-xs font-semibold"
                        :class="TagColors[tag]"
                    >
                        <Icon :name="TagIcons[tag]" />
                        {{ TagNames[tag] }}</Badge
                    >
                </div>
            </section>

            <section>
                <p class="text-text font-medium text-sm mt-3">Description</p>
                <p class="text-muted-foreground text-sm mb-4 mt-1">
                    {{ program?.description }}
                </p>
            </section>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-2 items-start">
                <div
                    v-for="day in program?.days"
                    :key="day.day_number"
                    class="rounded-xl border-primary-dark border collapse collapse-arrow last:mb-6 md:last:mb-3"
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
            <Dialog v-if="!isStarted">
                <DialogTrigger
                    class="sticky mt-auto bottom-10 md:w-60 md:self-end"
                >
                    <Button
                        variant="success"
                        class="mt-auto w-full py-6 md:py-5"
                        >Start</Button
                    >
                </DialogTrigger>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Start program</DialogTitle>
                        <DialogDescription>
                            Do you want to start this program?
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
                class="grid grid-cols-1 md:grid-cols-[2fr_1fr] gap-1 w-full mt-auto sticky bottom-10"
            >
                <Dialog>
                    <DialogTrigger>
                        <Button variant="success" class="w-full py-5"
                            >Mark completed <span class="ml-1">🎉</span></Button
                        >
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Congratulations 🎉</DialogTitle>
                            <DialogDescription>
                                Do you want to mark this program as completed?
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
                        <Button variant="destructive" class="w-full py-5"
                            >Cancel</Button
                        >
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Cancel program</DialogTitle>
                            <DialogDescription>
                                Do you want to cancel this program?
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
        </section>
    </article>
</template>
<script setup lang="ts">
import { Api } from "~/api/api";
import Badge from "~/components/ui/badge/Badge.vue";
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
import { TagColors, TagIcons, TagNames } from "~/constants/tags";
import type { Program } from "~/models/program.model";
import type { UserActivity } from "~/models/user_activity.model";

const route = useRoute();
const userStore = useUserStore();

const { data: program } = await useFetch<Program>(
    `/api/programs/${route.params.id}`,
);

console.log(program.value);

const { data: activity_log } =
    await useFetch<UserActivity[]>(`/api/user-activities`);

const startedActivity = computed(() => {
    return activity_log.value?.find(
        (log) => log.program_id == program.value?.id && log.end_date === null,
    );
});
const isStarted = computed(() => {
    return startedActivity.value !== undefined;
});

async function completeActivity() {
    try {
        await Api.completeActivity(startedActivity.value!.id!);
        activity_log.value = activity_log.value?.filter(
            (log) => log.id !== startedActivity.value?.id,
        );
    } catch (err) {
        console.error("Error completing activity:", err);
    }
}

async function startActivity() {
    try {
        const newActivity = await Api.startActivity(null, program.value!.id!);

        activity_log.value = [...(activity_log.value || []), newActivity];
    } catch (err) {
        console.error("Error starting activity:", err);
    }
}

async function cancelActivity() {
    try {
        await Api.cancelActivity(startedActivity.value!.id!);
        activity_log.value = activity_log.value?.filter(
            (log) => log.id !== startedActivity.value?.id,
        );
    } catch (err) {
        console.error("Error cancelling activity:", err);
    }
}
</script>
