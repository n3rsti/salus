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

            <p class="text-sm text-gray-600">
                This application uses cookies and similar technologies to ensure
                proper operation, enhance user experience, and maintain system
                security.
                <br />
                In accordance with the General Data Protection Regulation
                (GDPR), the system processes only the minimum data necessary for
                its functionality. User consent is explicitly required before
                any non-essential data is stored or processed. Users have the
                right to access, export, and request the deletion of their
                personal data at any time.
                <br />
                All data is protected using encryption both in transit and at
                rest. Security measures such as access control, request rate
                limiting, anomaly detection, abuse prevention, regular backups,
                and key rotation are implemented to safeguard stored
                information.
                <br />
                Where possible, data is pseudonymized and never used for
                purposes other than those required for the operation of the
                application. No data is shared with third parties without
                explicit user consent.
                <br />
                This application is intended for informational and educational
                purposes only and does not constitute professional medical
                advice. Users should always consult qualified professionals for
                medical decisions.
                <br />
                By clicking “I agree”, you confirm that you have read and
                understood this notice and consent to the use of cookies and
                data processing as described above.
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
