<template>
    <div class="min-h-screen w-full flex flex-col">
        <main class="grow bg-neutral-100 font-display flex justify-center">
            <slot />
        </main>
        <footer
            class="flex justify-evenly h-1/12 left-0 right-0 p-2 bg-green-500 text-white"
        >
            <NuxtLink to="/cookies">Cookies</NuxtLink>
            <NuxtLink to="https://github.com/n3rsti/salus">Github</NuxtLink>
            <NuxtLink to="https://github.com/n3rsti/salus/blob/main/LICENSE"
                >License</NuxtLink
            >
        </footer>
    </div>
</template>
