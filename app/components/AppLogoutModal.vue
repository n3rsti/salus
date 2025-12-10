<script setup lang="ts">
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";

import { SidebarMenuButton } from "@/components/ui/sidebar";
import { LogOut } from "lucide-vue-next";
import { Button } from "./ui/button";

async function logout() {
    await $fetch("/api/auth/logout", {
        method: "POST",
        onResponse: async (response) => {
            if (response.response.status == 200) {
                const userStore = useUserStore();
                userStore.$reset();
                await navigateTo("/login");
            } else {
                console.error("Logout failed. Please try again.");
            }
        },
    });
}
</script>

<template>
    <Dialog>
        <DialogTrigger class="w-full">
            <SidebarMenuButton>
                <NuxtLink class="flex items-center gap-2 font-semibold">
                    <LogOut class="size-4" />
                    <span>Logout</span>
                </NuxtLink>
            </SidebarMenuButton>
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Are you sure you want to log out?</DialogTitle>
                <DialogDescription>
                    You will need to log in again to access your account.
                </DialogDescription>
            </DialogHeader>
            <DialogFooter>
                <Button variant="destructive" @click="logout">Log out</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>
