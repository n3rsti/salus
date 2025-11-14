import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
    state: () => {
        return { username: "" };
    },

    persist: true,
});
