<template>
    <SidebarProvider>
        <div
            class="min-h-screen bg-primary-foreground font-display flex flex-col"
        >
            <AppSidebar />
            <NavBar class="fixed h-16 z-10" @toggle_sidebar="toggleSidebar" />
            <main class="p-4 sm:p-8 flex flex-col grow mt-16 lg:ml-60">
                <slot />
            </main>
        </div>
    </SidebarProvider>
</template>

<script setup lang="ts">
import AppSidebar from "@/components/AppSidebar.vue";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
const isSidebarOpen = ref<boolean>(false);

function toggleSidebar() {
    isSidebarOpen.value = !isSidebarOpen.value;
}
</script>
