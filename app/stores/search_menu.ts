import { defineStore } from "pinia";

export const useSearchStore = defineStore("search", {
    state: () => {
        return { isOpen: false };
    },
    actions: {
        close() {
            this.isOpen = false;
        },
        open() {
            this.isOpen = true;
        },
    },
});
