import { defineStore } from "pinia";

type ActiveTab = "activities" | "";

export const useSearchStore = defineStore("search", {
    state: () => {
        return { isOpen: false, activeTab: "" as ActiveTab };
    },
    actions: {
        close() {
            this.isOpen = false;
            this.activeTab = "";
        },
        open() {
            this.isOpen = true;
        },
    },
});
