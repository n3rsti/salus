const allowed_routes = ["/login", "/register",];

export default defineNuxtRouteMiddleware((to) => {
    const store = useUserStore();

    if (!allowed_routes.includes(to.path) && store.username == "") {
        return navigateTo("/login");
    }
});
