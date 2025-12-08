<template>
    <Sidebar class="mt-16 bg-white">
        <SidebarHeader class="bg-green-500 text-white">
            <SidebarMenu>
                <SidebarMenuItem>
                    <SidebarMenuButton
                        size="lg"
                        class="hover:bg-green-600 hover:text-white"
                    >
                        <div
                            class="grid flex-1 text-left text-sm leading-tight"
                        >
                            <span class="truncate font-semibold">{{
                                store.username
                            }}</span>
                            <span class="truncate text-xs">User</span>
                        </div>
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
                                <NuxtLink :to="item.url">
                                    <component :is="item.icon" />
                                    <span>{{ item.title }}</span>
                                </NuxtLink>
                            </SidebarMenuButton>
                        </SidebarMenuItem>
                    </SidebarMenu>
                </SidebarGroupContent>
            </SidebarGroup>
        </SidebarContent>
    </Sidebar>
</template>

<script setup lang="ts">
import {
    Sidebar,
    SidebarContent,
    SidebarHeader,
} from "@/components/ui/sidebar";
import { Calendar, Home, Dumbbell, Smile, ListChecks } from "lucide-vue-next";
import {
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar";

interface MenuItem {
    title: string;
    url: string;
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
];

const store = useUserStore();
</script>
