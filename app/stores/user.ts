import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
    state: () => {
        return { username: "", id: 0 };
    },

    persist: true,
});
