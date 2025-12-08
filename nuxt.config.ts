// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
    compatibilityDate: "2025-07-15",
    devtools: { enabled: true },
    modules: [
      "@nuxt/eslint",
      "@nuxt/icon",
      "@nuxt/fonts",
      "@pinia/nuxt",
      "pinia-plugin-persistedstate/nuxt",
      "shadcn-nuxt",
    ],
    css: ["./app/assets/css/main.css"],
    vite: {
        plugins: tailwindcss(),
    },
    fonts: {
        defaults: {
            weights: [200, 300, 400, 500, 600, 700, 800, 900],
        },
    },
    icon: {
        localApiEndpoint: "/icons/_nuxt_icon",
    },
    nitro: {
        routeRules: {
            "/api/**": {
                proxy: process.env.API_BASE_URL
                    ? process.env.API_BASE_URL + "/**"
                    : "http://salus-api:8080/api/**",
            },
        },
    },
});