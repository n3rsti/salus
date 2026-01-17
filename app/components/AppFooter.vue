<template>
    <footer
        class="flex flex-col items-center justify-center py-5 h-[15vh] bg-green-500 text-white gap-1"
    >
        <Icon
            class="text-4xl"
            name="material-symbols:digital-wellbeing-rounded"
        />
        <h3 class="font-semibold text-lg">Salus</h3>

        <section
            class="flex items-center justify-center gap-4 w-full text-center text-sm mt-2"
        >
            <NuxtLink to="/cookies">Cookies</NuxtLink>
            <NuxtLink to="https://github.com/n3rsti/salus">Github</NuxtLink>
            <NuxtLink to="https://github.com/n3rsti/salus/blob/main/LICENSE"
                >License</NuxtLink
            >
        </section>
    </footer>
</template>
