<template>
    <div class="min-h-screen bg-neutral-100 font-display flex flex-col">
        <NavBar />
        <main class="p-4 sm:p-8 md:px-10 lg:px-14 flex flex-col grow">
            <slot />
        </main>
    </div>
</template>
