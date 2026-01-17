import type { UserActivity } from "~/models/user_activity.model";

export const Api = {
    completeActivity: async (id: number) => {
        const { $api } = useNuxtApp();
        return await $api(`/api/user-activities/${id}/complete`, {
            method: "POST",
        });
    },

    startActivity: async (
        activityId: number | null,
        programId: number | null,
    ) => {
        const { $api } = useNuxtApp();
        return $api<UserActivity>(`/api/user-activities`, {
            method: "POST",
            body: {
                activity_id: activityId,
                program_id: programId,
            },
        });
    },

    cancelActivity: async (id: number) => {
        const { $api } = useNuxtApp();
        return await $api(`/api/user-activities/${id}`, {
            method: "DELETE",
        });
    },
};
