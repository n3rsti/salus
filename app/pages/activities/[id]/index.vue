<template>
    <section class="flex flex-col grow gap-3">
        <article
            class="flex flex-col border rounded-xl p-3 sm:p-5 md:p-6 lg:p-7 bg-primary-light border-neutral-100 border-t border-t-transparent shadow grow"
        >
            <div class="relative">
                <img
                    :src="'/media/' + activity?.image_url"
                    alt=""
                    class="object-cover w-full h-60 rounded-xl shadow border-primary-light border-t-transparent"
                />

                <Icon
                    v-if="activity?.owner?.role_id == Role.Trainer"
                    name="material-symbols:verified"
                    class="text-green-500 text-xl absolute right-3 top-3"
                    title="By verified trainer"
                />
            </div>
            <section class="flex flex-col grow p-2 mt-3 relative gap-3">
                <section class="flex">
                    <h1 class="font-bold text-3xl mt-1 text-primary">
                        {{ activity?.name }}
                        <Badge
                            v-if="activity"
                            class="text-xs rounded-md"
                            :class="DifficultiesColors[activity?.difficulty]"
                            >{{ Difficulties[activity.difficulty] }}</Badge
                        >
                    </h1>
                    <NuxtLink
                        v-if="
                            userStore.id == activity?.owner?.id ||
                            userStore.isAdmin()
                        "
                        :to="'/activities/' + route.params.id + '/edit'"
                        class="ml-auto"
                    >
                        <Button variant="default" class="ml-auto px-4"
                            >Edit</Button
                        >
                    </NuxtLink>
                </section>
                <section class="flex gap-8">
                    <section>
                        <p class="text-primary font-medium text-sm">Duration</p>
                        <p class="text-muted-foreground flex items-center">
                            <Icon class="" name="ic:outline-access-time" />
                            <span class="ml-1 text-sm"
                                >{{ activity?.duration_minutes }} minutes</span
                            >
                        </p>
                    </section>
                    <section>
                        <p class="text-primary font-medium text-sm">Author</p>
                        <NuxtLink
                            class="font-semibold text-sm"
                            :to="'/profile/' + activity?.owner?.id"
                        >
                            {{ activity?.owner?.username }}
                        </NuxtLink>
                    </section>
                </section>

                <section>
                    <p class="text-primary font-medium text-sm">Tags</p>
                    <section class="flex gap-1 flex-wrap my-2">
                        <Badge
                            v-for="tag in activity?.tags"
                            :key="tag"
                            class="text-xs rounded-md p-0.5 px-1 text-center shadow-xs font-semibold"
                            :class="TagColors[tag]"
                        >
                            <Icon :name="TagIcons[tag]" />
                            {{ TagNames[tag] }}</Badge
                        >
                    </section>
                </section>

                <section>
                    <p class="text-primary font-medium text-sm">Description</p>
                    <p class="text-muted-foreground text-sm mb-4 mt-1">
                        {{ activity?.description }}
                    </p>
                </section>

                <section>
                    <p class="text-primary font-medium text-sm">Content</p>
                    <div class="text-muted-foreground text-sm mb-4 mt-1">
                        <template
                            v-for="(line, index) in parsedDescription"
                            :key="index"
                        >
                            <p
                                v-if="line.type === 'text'"
                                class="whitespace-pre-wrap"
                            >
                                {{ line.content || "\u00A0" }}
                            </p>
                            <div
                                v-else-if="line.type === 'youtube'"
                                class="my-4 rounded-lg overflow-hidden aspect-video"
                            >
                                <iframe
                                    :src="`https://www.youtube.com/embed/${line.videoId}`"
                                    class="aspect-video rounded-md max-w-md w-full"
                                    frameborder="0"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                    allowfullscreen
                                ></iframe>
                            </div>
                        </template>
                    </div>
                </section>

                <slot></slot>

                <Dialog v-if="!isStarted">
                    <DialogTrigger
                        class="sticky mt-auto bottom-10 w-full md:self-end"
                    >
                        <Button
                            variant="success"
                            class="mt-auto w-full py-6 md:py-5"
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
                    class="grid grid-cols-1 md:grid-cols-[2fr_1fr] gap-1 w-full mt-auto sticky bottom-10"
                >
                    <Dialog>
                        <DialogTrigger>
                            <Button variant="success" class="w-full py-5"
                                >Mark completed
                                <span class="ml-1">🎉</span></Button
                            >
                        </DialogTrigger>
                        <DialogContent>
                            <DialogHeader>
                                <DialogTitle>Congratulations 🎉</DialogTitle>
                                <DialogDescription>
                                    Do you want to mark this activity as
                                    completed?
                                </DialogDescription>
                            </DialogHeader>
                            <DialogFooter>
                                <Button
                                    variant="success"
                                    @click="completeActivity"
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
            </section>
        </article>

        <AppReviewCard
            :reviews="reviews"
            :is-reviewed="isReviewed"
            :reset-key="reviewResetKey"
            :average-rating="activity?.average_rating"
            @submit-review="handleReview"
            @delete-review="deleteReview"
        ></AppReviewCard>
    </section>
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
import { Role } from "~/constants/roles";
import { TagColors, TagIcons, TagNames } from "~/constants/tags";
import type { Activity } from "~/models/activity.model";
import type { Review } from "~/models/review.model";
import type { UserActivity } from "~/models/user_activity.model";

const route = useRoute();
const activityId = route.params.id;
const program = useRoute().query.program;
const parentProgramId = program ? Number(program) : null;
const dayId = useRoute().query.day ? Number(useRoute().query.day) : null;
const userStore = useUserStore();

const { data: activity } = await useFetch<Activity>(
    `/api/activities/${activityId}`,
);

const { data: reviews } = await useFetch<Review[]>(
    `/api/activities/${activityId}/reviews?user_id=${userStore.id}`,
);

const isReviewed = computed(() => {
    if (!reviews.value || reviews.value?.length == 0) return false;
    return reviews.value[0]?.user.id == userStore.id;
});

const reviewResetKey = ref(0);

const parsedDescription = computed(() => {
    if (!activity.value?.content) return [];

    const lines = activity.value.content.split("\n");
    const result: Array<{ type: string; content?: string; videoId?: string }> =
        [];

    const youtubeRegex =
        /((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:[\w-]+\?v=|embed\/|live\/|v\/)?)?([\w-]+)(\S+)?/;

    lines.forEach((line) => {
        const match = line.match(youtubeRegex);
        if (match && match[5]) {
            result.push({ type: "youtube", videoId: match[5] });
        } else {
            result.push({ type: "text", content: line });
        }
    });

    return result;
});

const { data: activity_log } =
    await useFetch<UserActivity[]>(`/api/user-activities`);

const startedActivity = computed(() => {
    if (program && dayId) {
        return activity_log.value?.find(
            (log) =>
                log.activity_id === activity.value?.id &&
                log.end_date === null &&
                log.program_id == Number(program) &&
                log.program_day_id == Number(dayId),
        );
    }
    return activity_log.value?.find(
        (log) =>
            log.activity_id === activity.value?.id &&
            log.end_date === null &&
            !log.program_id &&
            !log.program_day_id,
    );
});

console.log("Started activity for index:", startedActivity.value);

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
        const newActivity = await Api.startActivity(
            activity.value?.id || null,
            parentProgramId,
            dayId,
        );

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

async function handleReview(description: string, review: number) {
    const { $api } = useNuxtApp();
    try {
        const newReview = await $api<Review>(
            `/api/activities/${activity.value?.id}/reviews`,
            {
                method: "POST",
                body: {
                    comment: description,
                    rating: review,
                },
            },
        );

        reviewResetKey.value++;
        reviews.value = [newReview, ...(reviews.value || [])];
    } catch (err) {
        console.error("Error posting review:", err);
    }
}

async function deleteReview(id: number) {
    const { $api } = useNuxtApp();
    try {
        await $api(`/api/reviews/${id}`, {
            method: "DELETE",
        });
        reviews.value = reviews.value?.filter((r) => r.id !== id);
    } catch (err) {
        console.error("Error deleting review:", err);
    }
}
</script>
