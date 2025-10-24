// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
    compatibilityDate: "2025-07-15",
    devtools: { enabled: true },
    modules: ["@nuxt/eslint", "@nuxt/icon", "@nuxt/fonts"],
    css: ["./app/assets/css/main.css"],
    vite: {
        plugins: tailwindcss(),
    },
    fonts: {
        defaults: {
            weights: [400, 500, 600, 700, 800, 900],
        },
    },
});

