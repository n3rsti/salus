export default defineNuxtRouteMiddleware(async () => {
    try {
        await $fetch("/api/user-preferences/me", {
            credentials: "include",
        });
    } catch (error: any) {
        if (error?.status === 404) {
            const requiresSurvey = useState<boolean>(
                "requiresSurvey",
                () => true,
            );
            requiresSurvey.value = true;
        }
    }
});
