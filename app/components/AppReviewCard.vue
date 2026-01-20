<template>
    <section
        class="flex flex-col gap-3 border rounded-xl p-3 sm:p-5 md:p-6 lg:p-7 bg-primary-light border-neutral-100 border-t border-t-transparent shadow"
    >
        <section class="flex items-center gap-2">
            <h2 class="font-medium">Reviews</h2>
            <section v-if="props.averageRating" class="flex items-center gap-1">
                <Icon
                    name="material-symbols:star-rounded"
                    class="text-yellow-400 text-xl"
                />
                <p class="text-xs font-medium">
                    {{ props.averageRating.toFixed(1) }}
                </p>
            </section>
            <template v-else>
                <span class="text-muted-foreground text-xs">No rating</span>
            </template>
        </section>
        <form
            v-if="!isReviewed"
            action=""
            class="flex flex-col gap-3"
            @submit.prevent="submitForm"
        >
            <Textarea
                id="review"
                v-model="description"
                name="review"
                placeholder="Write about your experience..."
                required
            ></Textarea>
            <section class="flex gap-1">
                <div v-for="star of 5" :key="star">
                    <input
                        :id="`star-${star}`"
                        v-model="rating"
                        type="radio"
                        name="rating"
                        :value="star"
                        class="w-0"
                        required
                    />
                    <label
                        :for="`star-${star}`"
                        :class="
                            star <= rating ? 'text-yellow-500' : 'text-gray-200'
                        "
                    >
                        <Icon
                            name="material-symbols:star-rounded"
                            class="text-3xl cursor-pointer"
                        />
                    </label>
                </div>
                <Button variant="default" class="ml-auto">Post review</Button>
            </section>
        </form>
        <section class="flex flex-col gap-5">
            <article
                v-for="review of props.reviews"
                :key="review.id"
                class="flex flex-col gap-2"
            >
                <section class="flex gap-2 items-center">
                    <p class="text-sm font-medium">
                        {{ review.user.username }}
                    </p>
                    <p class="text-xs text-muted-foreground">
                        {{ formatTimeAgo(review.created_at) }}
                    </p>
                    <Dialog>
                        <DropdownMenu v-if="review.user.id == userStore.id">
                            <DropdownMenuTrigger class="ml-auto">
                                <Icon
                                    name="mdi:dots-vertical"
                                    class="text-xl"
                                />
                            </DropdownMenuTrigger>
                            <DropdownMenuContent>
                                <DropdownMenuItem>Edit </DropdownMenuItem>
                                <DialogTrigger as-child>
                                    <DropdownMenuItem variant="destructive"
                                        >Delete
                                    </DropdownMenuItem>
                                </DialogTrigger>
                            </DropdownMenuContent>
                        </DropdownMenu>
                        <DialogContent>
                            <DialogHeader>
                                <DialogTitle>Delete review</DialogTitle>
                                <DialogDescription>
                                    Are you sure you want to delete your review?
                                </DialogDescription>
                            </DialogHeader>
                            <DialogFooter>
                                <Button
                                    type="submit"
                                    variant="destructive"
                                    @click="deleteReview(review.id)"
                                    >Delete</Button
                                >
                            </DialogFooter>
                        </DialogContent>
                    </Dialog>
                </section>
                <section class="flex items-center">
                    <Icon
                        v-for="star of 5"
                        :key="star"
                        name="material-symbols:star-rounded"
                        class="text-xl"
                        :class="
                            star <= review.rating
                                ? 'text-yellow-500'
                                : 'text-gray-200'
                        "
                    />
                </section>
                <section>
                    <p class="text-xs text-muted-foreground">
                        {{ review.comment }}
                    </p>
                </section>
            </article>
        </section>
    </section>
</template>
<script setup lang="ts">
import type { Review } from "~/models/review.model";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
    Dialog,
    DialogFooter,
    DialogHeader,
    DialogContent,
    DialogDescription,
    DialogTitle,
    DialogTrigger,
} from "./ui/dialog";

const description = ref("");
const rating = ref<number>(0);

const userStore = useUserStore();

const props = defineProps<{
    reviews?: Review[];
    isReviewed: boolean;
    resetKey: number;
    averageRating?: number;
}>();

watch(
    () => props.resetKey,
    () => {
        description.value = "";
        rating.value = 0;
    },
);

const emit = defineEmits<{
    submitReview: [description: string, rating: number];
    deleteReview: [id: number];
}>();

function submitForm() {
    emit("submitReview", description.value, rating.value);
}

function deleteReview(id: number) {
    emit("deleteReview", id);
}

function formatTimeAgo(date: Date | string | number): string {
    const dateObj = new Date(date);
    const now = new Date();
    const diffMs = now.getTime() - dateObj.getTime();
    const diffSeconds = Math.floor(diffMs / 1000);
    const diffMinutes = Math.floor(diffSeconds / 60);
    const diffHours = Math.floor(diffMinutes / 60);

    if (diffSeconds < 60) {
        return `${diffSeconds} second${diffSeconds !== 1 ? "s" : ""} ago`;
    } else if (diffMinutes < 60) {
        return `${diffMinutes} minute${diffMinutes !== 1 ? "s" : ""} ago`;
    } else if (diffHours < 24) {
        return `${diffHours} hour${diffHours !== 1 ? "s" : ""} ago`;
    } else {
        const day = dateObj.getDate();
        const month = dateObj.toLocaleString("en-US", { month: "long" });
        const year = dateObj.getFullYear();
        return `${day} ${month} ${year}`;
    }
}
</script>
