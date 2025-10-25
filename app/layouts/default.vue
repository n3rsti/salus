<template>
    <div class="min-h-screen bg-neutral-100 font-display flex flex-col">
        <NavBar class="fixed h-20 z-10" @toggle_sidebar="toggleSidebar" />
        <AppSidebar
            :is-open="isSidebarOpen"
            @toggle-sidebar="toggleSidebar"
        ></AppSidebar>
        <main class="p-4 sm:p-8 flex flex-col grow mt-20 lg:ml-60">
            <slot />
        </main>
    </div>
</template>

<script setup lang="ts">
const isSidebarOpen = ref<boolean>(false);

function toggleSidebar() {
    isSidebarOpen.value = !isSidebarOpen.value;
}
</script>
