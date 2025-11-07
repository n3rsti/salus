<template>
    <main class="flex flex-col justify-center items-center content-center p-4">
        <NuxtLink class="absolute top-4 left-4 text-white" to="/"
            ><AppButton :color="'green'">
                <Icon
                    class="text-4xl"
                    name="dashicons:admin-home"
                /> </AppButton
        ></NuxtLink>
        <form
            class="rounded-xl bg-primary-light text-green-700 p-8 w-11/12 shadow border-neutral-100 border-t border-t-transparent"
            @submit.prevent="handleLogin"
        >
            <h2 class="text-green-500 font-semibold text-3xl">
                Log in to salus
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
            <div class="validator-hint hidden">Enter valid email address</div>

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
                    autocomplete="current-password"
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
                <br />At least one uppercase letter
            </p>

            <AppButton
                class="w-full shadow-sm border-t-transparent text-white mt-4"
                :color="'green'"
                type="submit"
            >
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
            </AppButton>

            <p class="mt-4">
                Not yet a user?<br />
                <NuxtLink
                    class="text-green-900 underline hover:text-green-600"
                    to="/register"
                    >Sign up</NuxtLink
                >
            </p>

            <button
                class="btn bg-white text-black border-green-500 w-full mt-10 hover:bg-gray-300"
            >
                <Icon name="logos:microsoft-icon" />
                Login with Microsoft
            </button>
            <button
                class="btn bg-white text-black border-blue-500 w-full mt-4 hover:bg-gray-300"
            >
                <Icon name="logos:google-icon" />
                Login with Google
            </button>
            <button
                class="btn bg-white text-black border-black w-full mt-4 hover:bg-gray-300"
            >
                <Icon name="logos:github-icon" />
                Login with Github
            </button>
        </form>
    </main>
</template>
<script setup lang="ts">
definePageMeta({
    layout: "authentication",
});

const email = ref("");
const password = ref("");
async function handleLogin() {
    alert("✅ Login successful!");
}
</script>
