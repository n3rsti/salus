<template>
    <div class="flex flex-col justify-center items-center content-center p-4">
        <form
            class="rounded-xl bg-primary-light text-green-700 p-8 w-11/12 max-w-[560px] min-w-[300px] shadow border-neutral-100 border-t border-t-transparent"
            @submit.prevent="handleRegister"
        >
            <h2 class="text-green-500 font-semibold text-3xl">
                Sign up to salus
            </h2>
            <label
                class="input validator bg-amber-50 border-2 border-primary-dark rounded-xl focus-within:border-green-500 w-full mt-8"
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
            <p class="validator-hint hidden">Enter valid email address</p>
            <label
                class="input validator bg-amber-50 border-2 border-primary-dark rounded-xl focus-within:border-green-500 w-full mt-4"
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
                            d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"
                        ></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </g>
                </svg>
                <input
                    v-model="username"
                    autocomplete="username"
                    type="text"
                    required
                    placeholder="Username"
                    pattern="[A-Za-z][A-Za-z0-9\-]*"
                    minlength="3"
                    maxlength="30"
                    title="Only letters, numbers or dash"
                />
            </label>
            <p class="validator-hint hidden">
                Must be 3 to 30 characters
                <br />containing only letters, numbers or dash
            </p>
            <label
                class="input validator bg-amber-50 border-2 border-primary-dark rounded-xl focus-within:border-green-500 mt-4 w-full"
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
                    autocomplete="new-password"
                    type="password"
                    required
                    placeholder="Password"
                    minlength="8"
                    pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                    title="Must be more than 8 characters, including number, lowercase letter, uppercase letter"
                />
            </label>
            <label
                class="input validator bg-amber-50 border-2 border-primary-dark rounded-xl focus-within:border-green-500 mt-4 w-full"
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
                    v-model="passwordConfirm"
                    autocomplete="new-password"
                    type="password"
                    required
                    placeholder="Password"
                    minlength="8"
                    pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                    title="Must be more than 8 characters, including number, lowercase letter, uppercase letter"
                />
            </label>
            <p class="validator-hint hidden">
                Must be more than 8 characters, including
                <br />At least one number <br />At least one lowercase letter
                <br />At least one uppercase letter <br />Passwords needs to be
                the same
            </p>
            <Button
                class="w-full shadow-sm border-t-transparent text-white mt-4"
                variant="success"
            >
                Sign up
            </Button>
        </form>
        <NuxtLink
            class="text-green-900 underline hover:text-green-600 mt-4"
            to="/login"
            >Go to Login</NuxtLink
        >
    </div>
</template>

<script setup lang="ts">
import { Button } from "~/components/ui/button";

definePageMeta({
    layout: "authentication",
});

const email = ref("");
const username = ref("");
const password = ref("");
const passwordConfirm = ref("");
async function handleRegister() {
    if (password.value != passwordConfirm.value) {
        passwordConfirm.value = "";
        return;
    }
    await $fetch("/api/users", {
        method: "POST",
        body: {
            email: email.value,
            username: username.value,
            password: password.value,
            role_id: 1,
        },
        onResponse: (response) => {
            if (response.response.status == 201) {
                alert("Registration completed successfully");
                navigateTo("/login");
            } else {
                console.log(response.error);
                alert("Invalid registration");
            }
        },
    });
}
</script>
