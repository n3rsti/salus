<template>
    <div
        v-if="store.loaded && !store.accepted"
        class="fixed inset-0 z-50 flex items-center justify-center"
    >
        <div class="absolute inset-0 bg-black/60"></div>
        <div
            class="relative bg-white rounded-xl p-6 max-w-md w-full shadow-xl text-center space-y-4"
        >
            <h2 class="text-xl font-semibold">
                Cookie & Data Processing Notice
            </h2>

            <p class="text-sm text-gray-600 text-left">
                Cookie & Data Processing Notice This application uses cookies
                and similar technologies to ensure proper functionality,
                security, and an improved user experience. The minimum necessary
                data is processed. No personal data is stored or processed
                without explicit user consent. <br />By clicking “I agree”, you
                consent to the use of cookies and data processing as described.
            </p>

            <Button
                class="px-4 py-2 rounded bg-green-600 text-white hover:bg-green-500 transition"
                @click="store.accept"
            >
                I agree
            </Button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useCookieConsentStore } from "@/stores/cookie_consent";
import { Button } from "./ui/button";

const store = useCookieConsentStore();
</script>
