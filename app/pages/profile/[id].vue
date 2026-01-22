<script setup lang="ts">
import { Button } from "~/components/ui/button";
import {
    Dialog,
    DialogFooter,
    DialogHeader,
    DialogContent,
    DialogDescription,
    DialogTitle,
    DialogTrigger,
    DialogClose,
} from "~/components/ui/dialog";
import { Skeleton } from "~/components/ui/skeleton";
import { Role } from "~/constants/roles";
import type { Activity } from "~/models/activity.model";
import type { Program } from "~/models/program.model";
import type { User } from "~/models/user.model";

definePageMeta({
    public: true,
});

const userStore = useUserStore();

const route = useRoute();
const user_id = route.params.id;

const { data: user } = useFetch<User>(`/api/users/${user_id}`);

const { data: programs } = useFetch<Program[]>(
    `/api/programs?user_id=${user_id}&limit=10`,
);
const { data: activities } = useFetch<Activity[]>(
    `/api/activities?user_id=${user_id}&light=true&limit=10`,
);

const { $api } = useNuxtApp();

async function handleVerify() {
    const updatedUser = await $api<User>(`/api/users/${user_id}`, {
        method: "PUT",
        body: {
            role_id: Role.Trainer,
        },
    });
    user.value = updatedUser;
}

async function handleRevoke() {
    const updatedUser = await $api<User>(`/api/users/${user_id}`, {
        method: "PUT",
        body: {
            role_id: Role.User,
        },
    });
    user.value = updatedUser;
}

async function handleMakeAdmin() {
    const updatedUser = await $api<User>(`/api/users/${user_id}`, {
        method: "PUT",
        body: {
            role_id: Role.Admin,
        },
    });
    user.value = updatedUser;
}

async function handleRevokeAdmin() {
    const updatedUser = await $api<User>(`/api/users/${user_id}`, {
        method: "PUT",
        body: {
            role_id: Role.User,
        },
    });

    user.value = updatedUser;
}

async function fetchMorePrograms(limit: number) {
    const current = programs.value ?? [];
    if (current.length === 0) return;

    const { data, error } = await useFetch<Program[]>(
        `/api/programs?skip=${current.length}&limit=${limit}`,
    );

    if (error.value) return;

    const more = data.value ?? [];
    if (more.length === 0) return;

    programs.value = [...current, ...more];
}

async function fetchMoreActivities(limit: number) {
    const current = activities.value ?? [];
    if (current.length === 0) return;

    const { data, error } = await useFetch<Activity[]>(
        `/api/activities?light=true&skip=${current.length}&limit=${limit}`,
    );

    if (error.value) return;

    const more = data.value ?? [];
    if (more.length === 0) return;

    activities.value = [...current, ...more];
}
</script>

<template>
    <div class="flex flex-col gap-3">
        <div
            class="p-4 rounded-xl bg-primary-light flex justify-between items-center gap-2 shadow-sm"
        >
            <div class="flex items-center">
                <h1 class="text-green-700 text-xl font-semibold">
                    {{ user?.username }}
                </h1>
                <Icon
                    v-if="user?.role_id == Role.Trainer"
                    name="material-symbols:verified"
                    class="text-xl text-green-500"
                    title="Verified trainer"
                />
            </div>
            <div
                v-if="
                    (userStore?.role == Role.Admin ||
                        userStore?.role == Role.SuperAdmin) &&
                    userStore.id != user?.id
                "
                class="flex gap-1"
            >
                <Dialog v-if="user?.role_id == Role.User">
                    <DialogTrigger as-child>
                        <Button variant="success"
                            >Verify trainer

                            <Icon
                                name="material-symbols:verified"
                                class="text-lg text-white"
                            />
                        </Button>
                    </DialogTrigger>
                    <DialogContent class="sm:max-w-[425px]">
                        <DialogHeader>
                            <DialogTitle>Verify trainer</DialogTitle>
                            <DialogDescription>
                                Are you sure you want to verify this trainer?
                            </DialogDescription>
                        </DialogHeader>
                        <DialogFooter>
                            <DialogClose as-child>
                                <Button variant="outline"> Cancel </Button>
                            </DialogClose>
                            <Button
                                type="submit"
                                variant="success"
                                @click="handleVerify"
                                >Verify</Button
                            >
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
                <Dialog v-else-if="user?.role_id == Role.Trainer">
                    <DialogTrigger as-child>
                        <Button variant="destructive"
                            >Revoke trainer status
                        </Button>
                    </DialogTrigger>
                    <DialogContent class="sm:max-w-[425px]">
                        <DialogHeader>
                            <DialogTitle>Revoke trainer status</DialogTitle>
                            <DialogDescription>
                                Are you sure you want to revoke this trainer
                                status?
                            </DialogDescription>
                        </DialogHeader>
                        <DialogFooter>
                            <DialogClose as-child>
                                <Button variant="outline"> Cancel </Button>
                            </DialogClose>
                            <Button
                                type="submit"
                                variant="destructive"
                                @click="handleRevoke"
                                >Revoke</Button
                            >
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
                <Dialog
                    v-if="
                        userStore?.role == Role.SuperAdmin &&
                        user?.role_id != Role.Admin
                    "
                >
                    <DialogTrigger as-child>
                        <Button variant="default"> Add admin role </Button>
                    </DialogTrigger>
                    <DialogContent class="sm:max-w-[425px]">
                        <DialogHeader>
                            <DialogTitle>Add admin role</DialogTitle>
                            <DialogDescription>
                                Are you sure you want to add this user as admin?
                            </DialogDescription>
                        </DialogHeader>
                        <DialogFooter>
                            <DialogClose as-child>
                                <Button variant="outline"> Cancel </Button>
                            </DialogClose>
                            <Button
                                type="submit"
                                variant="default"
                                @click="handleMakeAdmin"
                                >Confirm</Button
                            >
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
                <Dialog
                    v-if="
                        userStore?.role == Role.SuperAdmin &&
                        user?.role_id == Role.Admin
                    "
                >
                    <DialogTrigger as-child>
                        <Button variant="default">Revoke admin role</Button>
                    </DialogTrigger>
                    <DialogContent class="sm:max-w-[425px]">
                        <DialogHeader>
                            <DialogTitle>Revoke admin role</DialogTitle>
                            <DialogDescription>
                                Are you sure you want to revoke this user as
                                admin?
                            </DialogDescription>
                        </DialogHeader>
                        <DialogFooter>
                            <DialogClose as-child>
                                <Button variant="outline"> Cancel </Button>
                            </DialogClose>
                            <Button
                                type="submit"
                                variant="default"
                                @click="handleRevokeAdmin"
                                >Confirm</Button
                            >
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>
        </div>

        <div class="flex flex-col gap-6 mt-4">
            <Card class="flex flex-col">
                <h2 class="text-lg font-semibold">
                    Created programs
                    <span v-if="false" class="text-sm text-muted-foreground"
                        >({{ programs?.length }})</span
                    >
                </h2>

                <div
                    v-if="!programs"
                    class="flex flex-col rounded-md py-2 px-2 gap-2"
                >
                    <div class="flex items-center gap-2">
                        <Skeleton class="h-8 aspect-square rounded-lg" />
                        <Skeleton class="w-20 h-4 rounded-md" />
                        <Skeleton class="w-12 h-5 rounded-md" />
                        <Skeleton class="ml-auto w-20 h-5 rounded-md" />
                    </div>
                    <Skeleton class="w-full h-5 rounded-md" />
                </div>

                <p v-if="programs?.length == 0" class="text-gray-500">
                    No programs yet.
                </p>

                <section class="flex flex-col gap-2">
                    <NuxtLink
                        v-for="program in programs"
                        :key="program.id"
                        :to="'/programs/' + program.id"
                        class="first:mt-2"
                    >
                        <AppVerticalCard :img="program.image_url">
                            <template #name>
                                {{ program.name }}
                            </template>
                            <template #badge>
                                <template v-if="program.average_rating">
                                    <Icon
                                        name="material-symbols:star-rounded"
                                        class="text-yellow-400 text-xl"
                                    />
                                    <p class="text-xs font-medium">
                                        {{ program.average_rating.toFixed(1) }}
                                    </p>
                                </template>
                            </template>

                            <template #description>
                                {{ program.description }}
                            </template>
                        </AppVerticalCard>
                    </NuxtLink>
                </section>

                <Button
                    v-if="programs && programs.length > 0"
                    class="mt-4 self-center"
                    variant="success"
                    @click="fetchMorePrograms(10)"
                >
                    Load more
                </Button>
            </Card>

            <Card class="flex flex-col">
                <h2 class="text-lg font-semibold">
                    Created activities
                    <span v-if="false" class="text-sm text-muted-foreground"
                        >({{ activities?.length }})</span
                    >
                </h2>

                <div
                    v-if="!activities"
                    class="flex flex-col rounded-md py-2 px-2 gap-2"
                >
                    <div class="flex items-center gap-2">
                        <Skeleton class="h-8 aspect-square rounded-lg" />
                        <Skeleton class="w-20 h-4 rounded-md" />
                        <Skeleton class="w-12 h-5 rounded-md" />
                        <Skeleton class="ml-auto w-20 h-5 rounded-md" />
                    </div>
                    <Skeleton class="w-full h-5 rounded-md" />
                </div>

                <p v-if="activities?.length == 0" class="text-gray-500">
                    No activities yet.
                </p>

                <section class="flex flex-col gap-2">
                    <NuxtLink
                        v-for="activity in activities"
                        :key="activity.id"
                        :to="'/activities/' + activity.id"
                        class="first:mt-2"
                    >
                        <AppVerticalCard :img="activity.image_url">
                            <template #name>
                                {{ activity.name }}
                            </template>

                            <template #badge>
                                <template v-if="activity.average_rating">
                                    <Icon
                                        name="material-symbols:star-rounded"
                                        class="text-yellow-400 text-xl"
                                    />
                                    <p class="text-xs font-medium">
                                        {{ activity.average_rating.toFixed(1) }}
                                    </p>
                                </template>
                            </template>

                            <template #description>
                                {{ activity.description }}
                            </template>
                        </AppVerticalCard>
                    </NuxtLink>
                </section>

                <Button
                    v-if="activities && activities.length > 0"
                    class="mt-4 self-center"
                    variant="success"
                    @click="fetchMoreActivities(10)"
                >
                    Load more
                </Button>
            </Card>
        </div>
    </div>
</template>
