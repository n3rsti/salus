<template>
    <SidebarProvider>
        <div class="flex flex-col">
            <AppGlobalSearch v-if="searchStore.activeTab === ''" />
            <div class="min-h-screen">
                <NavBar />
                <section class="flex">
                    <AppSidebar />
                    <section
                        class="bg-primary-foreground font-display flex flex-col w-full"
                    >
                        <main class="min-h-11/12 p-4 sm:p-8 flex flex-col grow">
                            <slot />
                        </main>
                    </section>
                </section>
            </div>
        </div>
    </SidebarProvider>
</template>

<script setup lang="ts">
import AppSidebar from "@/components/AppSidebar.vue";
import { SidebarProvider } from "@/components/ui/sidebar";

const searchStore = useSearchStore();
</script>
