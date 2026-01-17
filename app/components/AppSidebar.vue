<template>
    <Sidebar
        class="bg-white sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto"
        variant="sidebar"
    >
        <SidebarHeader class="bg-green-500 text-white">
            <SidebarMenu>
                <SidebarMenuItem>
                    <SidebarMenuButton
                        as-child
                        size="lg"
                        class="hover:bg-green-600 hover:text-white"
                    >
                        <NuxtLink
                            to="/profile"
                            class="grid flex-1 text-left text-sm leading-tight"
                        >
                            <span class="truncate font-semibold">
                                {{ store.username || "User" }}
                            </span>
                            <span class="truncate text-xs">User</span>
                        </NuxtLink>
                    </SidebarMenuButton>
                </SidebarMenuItem>
            </SidebarMenu>
        </SidebarHeader>
        <SidebarContent class="bg-white">
            <SidebarGroup v-for="section in menuSections" :key="section.label">
                <SidebarGroupLabel>{{ section.label }}</SidebarGroupLabel>
                <SidebarGroupContent>
                    <SidebarMenu>
                        <SidebarMenuItem
                            v-for="item in section.items"
                            :key="item.title"
                        >
                            <SidebarMenuButton as-child>
                                <NuxtLink
                                    v-if="item.url"
                                    :to="item.url"
                                    @click="toggle"
                                >
                                    <component :is="item.icon" />
                                    <span>{{ item.title }}</span>
                                </NuxtLink>
                                <component :is="item.icon" v-else />
                            </SidebarMenuButton>
                        </SidebarMenuItem>
                    </SidebarMenu>
                </SidebarGroupContent>
            </SidebarGroup>
        </SidebarContent>
    </Sidebar>
</template>

<script setup lang="ts">
import { Calendar, Home, Dumbbell, Smile, ListChecks } from "lucide-vue-next";
import {
    Sidebar,
    SidebarContent,
    SidebarHeader,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    useSidebar,
} from "@/components/ui/sidebar";
import AppLogoutModal from "./AppLogoutModal.vue";
import { useMediaQuery } from "@vueuse/core";

const { toggleSidebar } = useSidebar();

const isMobile = useMediaQuery("(max-width: 1024px)");

function toggle() {
    if (isMobile.value == true) {
        toggleSidebar();
    }
}

interface MenuItem {
    title: string;
    url?: string;
    icon: any;
}

interface MenuSection {
    label: string;
    items: MenuItem[];
}

const menuSections: MenuSection[] = [
    {
        label: "Application",
        items: [
            {
                title: "Home",
                url: "/",
                icon: Home,
            },
        ],
    },
    {
        label: "Workouts",
        items: [
            {
                title: "Programs",
                url: "/programs",
                icon: Calendar,
            },
            {
                title: "Activities",
                url: "/activities",
                icon: Dumbbell,
            },
        ],
    },
    {
        label: "Progress",
        items: [
            {
                title: "Mood Log",
                url: "/mood-log",
                icon: Smile,
            },
            {
                title: "Activity Log",
                url: "/activity-log",
                icon: ListChecks,
            },
        ],
    },
    {
        label: "Settings",
        items: [
            {
                title: "Log out",
                icon: AppLogoutModal,
            },
        ],
    },
];

const store = useUserStore();
</script>
