<template>
    <article class="flex flex-col gap-4">
        <section
            class="p-4 rounded-xl bg-primary-light flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">My requests</h1>
        </section>
        <section class="flex flex-col gap-3 justify-between">
            <article
                v-for="request in requests"
                :key="request.id"
                class="flex gap-3 items-center bg-primary-light shadow-sm rounded-xl p-4"
            >
                <NuxtLink
                    :to="'/requests/' + request.id"
                    class="hover:underline"
                >
                    <h2 class="text-sm font-semibold">
                        Trainer status request
                    </h2>
                </NuxtLink>
                <p class="text-sm text-muted-foreground">
                    {{ formatDate(request.created_at) }}
                </p>

                <Badge
                    :variant="request.resolved ? 'success' : 'destructive'"
                    class="py-0 text-xs"
                >
                    {{ request.resolved ? "Resolved" : "Unresolved" }}
                </Badge>
            </article>
        </section>
    </article>
</template>
<script setup lang="ts">
import { Badge } from "~/components/ui/badge";
import { formatDate } from "~/lib/utils";
import type { Request } from "~/models/request.model";

const userStore = useUserStore();

const { data: requests } = await useFetch<Request[]>(
    `/api/users/${userStore.id}/requests`,
);
</script>
