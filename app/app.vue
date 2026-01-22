<script setup lang="ts">
import { useCookieConsentStore } from "@/stores/cookie_consent";
const cookieStore = useCookieConsentStore();

onMounted(() => {
    cookieStore.load();
});
</script>
<template>
    <NuxtLayout>
        <NuxtPage />
    </NuxtLayout>
    <CookieConsent />
    <UserPreferencesSurvey />
</template>
