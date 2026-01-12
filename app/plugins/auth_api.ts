export default defineNuxtPlugin(() => {
    const api = $fetch.create({
        onResponseError({ response }) {
            if (response.status === 401) {
                const user = useUserStore();
                user.$reset();
                navigateTo("/login");
            }
        },
    });

    return {
        provide: {
            api,
        },
    };
});
