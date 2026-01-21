<template>
    <article>
        <section
            class="p-4 rounded-xl bg-primary-light mb-4 flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">
                Become a trainer
            </h1>
        </section>
        <section
            class="flex flex-col p-4 gap-3 rounded-xl bg-primary-light shadow-sm"
        >
            <h2 class="font-semibold flex col-span-full">
                Do you want to become a trainer?
            </h2>
            <p class="text-sm text-muted-foreground">
                Become a trainer and help others reach their fitness goals! You
                will receive a special badge to show your expertise. <br />You
                must show proof of your experience in the field of fitness.
            </p>
            <form
                action=""
                class="mt-3 flex flex-col gap-2"
                @submit.prevent="submitForm"
            >
                <div class="flex flex-col gap-2">
                    <Label for="description">Description</Label>
                    <Textarea
                        id="description"
                        v-model="description"
                        name="description"
                        placeholder="Describe your experience..."
                        :disabled="isPending"
                        required
                    ></Textarea>
                </div>
                <Button
                    v-if="!isPending"
                    type="submit"
                    variant="success"
                    class="w-full mt-3"
                    >Submit</Button
                >
                <p v-else class="text-sm">
                    You have already submitted a request for the trainer status.
                    Please wait for the response.
                </p>
            </form>
        </section>
    </article>
</template>
<script setup lang="ts">
import { Button } from "~/components/ui/button";
import { Label } from "~/components/ui/label";
import { Textarea } from "~/components/ui/textarea";
import type { Request } from "~/models/request.model";

const description = ref("");

const { $api } = useNuxtApp();

const userStore = useUserStore();
const isPending = computed(() => {
    if (!requests.value) return false;
    return requests.value.filter((r) => !r.resolved).length > 0;
});

const { data: requests } = await useFetch<Request[]>(
    `/api/users/${userStore.id}/requests`,
);

async function submitForm() {
    try {
        const newRequest = await $api<Request>("/api/requests", {
            method: "POST",
            body: {
                description: description.value,
            },
        });
        navigateTo("/requests/" + newRequest.id);
    } catch (error) {
        console.error("Error while creating request:", error);
    }
}
</script>
