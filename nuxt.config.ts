// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
    app: {
        head: {
            title: "Salus",
        },
    },
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
        devProxy: {
            '/api': {
                target: 'http://salus-api:8080',
                changeOrigin: true,
            },
        },
        routeRules: {
            '/api/**': {
                proxy: 'http://salus-api:8080/api/**',
            },
        },
    },
});
