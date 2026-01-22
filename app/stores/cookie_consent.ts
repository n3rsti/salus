import { defineStore } from "pinia";

export const useCookieConsentStore = defineStore("cookieConsent", {
    state: () => ({
        accepted: false,
        loaded: false,
    }),

    actions: {
        load() {
            const saved = localStorage.getItem("cookie-consent");
            this.accepted = saved === "true";
            this.loaded = true;
        },

        accept() {
            this.accepted = true;
            localStorage.setItem("cookie-consent", "true");
        },
    },
});
