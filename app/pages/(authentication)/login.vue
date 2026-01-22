<template>
    <div class="flex flex-col justify-center items-center content-center p-4">
        <form
            class="rounded-xl bg-primary-light text-green-700 p-8 w-11/12 shadow border-neutral-100 border-t border-t-transparent"
            @submit.prevent="handleLogin"
        >
            <h2 class="text-green-500 font-semibold text-3xl">
                Log in to salus
            </h2>
            <label
                class="input bg-amber-50 border-2 border-primary-dark rounded-xl focus-within:border-green-500 w-full mt-8"
            >
                <svg
                    class="h-[1em] opacity-50"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                >
                    <g
                        stroke-linejoin="round"
                        stroke-linecap="round"
                        stroke-width="2.5"
                        fill="none"
                        stroke="currentColor"
                    >
                        <rect width="20" height="16" x="2" y="4" rx="2"></rect>
                        <path
                            d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"
                        ></path>
                    </g>
                </svg>
                <input
                    v-model="email"
                    autocomplete="off"
                    type="email"
                    placeholder="mail@site.com"
                    required
                />
            </label>

            <label
                class="input bg-amber-50 border-2 border-primary-dark rounded-xl focus-within:border-green-500 mt-4 w-full"
            >
                <svg
                    class="h-[1em] opacity-50"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                >
                    <g
                        stroke-linejoin="round"
                        stroke-linecap="round"
                        stroke-width="2.5"
                        fill="none"
                        stroke="currentColor"
                    >
                        <path
                            d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"
                        ></path>
                        <circle
                            cx="16.5"
                            cy="7.5"
                            r=".5"
                            fill="currentColor"
                        ></circle>
                    </g>
                </svg>
                <input
                    v-model="password"
                    autocomplete="current-password"
                    type="password"
                    required
                    placeholder="Password"
                />
            </label>

            <Button class="w-full mt-4" variant="success" type="submit">
                <svg
                    aria-label="Email icon"
                    width="16"
                    height="16"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                >
                    <g
                        stroke-linejoin="round"
                        stroke-linecap="round"
                        stroke-width="2"
                        fill="none"
                        stroke="white"
                    >
                        <rect width="20" height="16" x="2" y="4" rx="2"></rect>
                        <path
                            d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"
                        ></path>
                    </g>
                </svg>
                <span class="ml-1">Login with Email</span>
            </Button>

            <p class="mt-4">
                Not yet a user?<br />
                <NuxtLink
                    class="text-green-900 underline hover:text-green-600"
                    to="/register"
                    >Sign up</NuxtLink
                >
            </p>
        </form>
    </div>
</template>
<script setup lang="ts">
import { Button } from "~/components/ui/button";
import type { Role } from "~/constants/roles";

definePageMeta({
    layout: "authentication",
});

const email = ref("");
const password = ref("");

interface Response {
    message: string;
    user: Record<string, string | number>;
}
async function handleLogin() {
    await $fetch<Response>("/api/auth/login", {
        method: "POST",
        body: {
            username_or_email: email.value,
            password: password.value,
        },
        onResponse: async (response) => {
            if (response.response.status == 200) {
                const data: Response = response.response._data;
                const userStore = useUserStore();

                userStore.username = (data.user.username as string) || null;
                userStore.id = (data.user.id as number) || 0;
                userStore.role = (data.user.role as Role) || null;
                userStore.email = (data.user.email as string) || null;
                await navigateTo("/");
            } else {
                password.value = "";
                email.value = "";
                alert("Username or password is wrong!");
            }
        },
    });
}
</script>
