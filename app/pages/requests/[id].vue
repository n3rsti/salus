<template>
    <article class="flex flex-col grow gap-3">
        <section
            class="p-4 rounded-xl bg-primary-light flex items-center justify-between shadow-sm"
        >
            <h1 class="text-green-700 text-xl font-semibold">
                Request {{ requestId }}
            </h1>
        </section>
        <section
            v-if="request && error == undefined"
            class="p-4 rounded-xl bg-primary-light flex flex-col gap-4 shadow-sm text-sm"
        >
            <section>
                <h3 class="font-semibold">Author</h3>
                <p class="text-sm">
                    {{ request.user.username }}
                </p>
            </section>

            <section>
                <h3 class="font-semibold">Created at</h3>
                <p class="text-sm">{{ formatDate(request.created_at) }}</p>
            </section>

            <section>
                <h3 class="font-semibold">Resolved</h3>
                <Badge
                    :variant="request.resolved ? 'success' : 'success'"
                    class="py-0 text-xs"
                >
                    {{ request.resolved }}
                </Badge>
            </section>

            <section>
                <h3 class="font-semibold">Description</h3>
                <p class="text-sm whitespace-pre-wrap">
                    {{ request.description }}
                </p>
            </section>
        </section>
        <section
            v-else-if="error"
            class="flex flex-col grow items-center justify-center"
        >
            <h2 class="text-2xl text-center font-semibold">Unauthorized</h2>
        </section>
        <section
            v-if="request?.response"
            class="p-4 rounded-xl bg-primary-light flex flex-col gap-4 shadow-sm text-sm"
        >
            <section>
                <h3 class="font-semibold">Admin</h3>
                <p class="text-sm">{{ request?.admin?.username }}</p>
            </section>

            <section v-if="request?.resolved_at">
                <h3 class="font-semibold">Resolved at</h3>
                <p class="text-sm">{{ formatDate(request?.resolved_at) }}</p>
            </section>

            <section>
                <h3 class="font-semibold">Response</h3>
                <p class="text-sm whitespace-pre-wrap">
                    {{ request?.response }}
                </p>
            </section>
        </section>
    </article>
</template>
<script setup lang="ts">
import { Badge } from "~/components/ui/badge";
import type { Request } from "~/models/request.model";

const route = useRoute();
const requestId = route.params.id;

const { data: request, error } = await useFetch<Request>(
    `/api/requests/${requestId}`,
);

const formatDate = (date: string | Date) => {
    return new Date(date).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
    });
};
</script>
