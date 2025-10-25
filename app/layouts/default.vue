<template>
    <div class="min-h-screen bg-neutral-100 font-display flex flex-col">
        <NavBar class="fixed h-20 z-10" />
        <main class="p-4 sm:p-8 md:px-10 lg:px-14 flex flex-col grow mt-20">
            <slot />
        </main>
    </div>
</template>
