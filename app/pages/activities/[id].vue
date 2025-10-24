<template>
    <article
        class="flex flex-col border rounded-xl p-3 sm:p-5 md:p-6 lg:p-7 bg-primary-light border-neutral-100 border-t border-t-transparent shadow grow"
    >
        <img
            :src="faker.image.url({ width: 800, height: 500 })"
            alt=""
            class="object-cover w-full h-32 rounded-xl shadow border-primary-light border-t-transparent"
        />
        <div class="flex flex-col grow p-2 mt-3">
            <div class="flex items-end">
                <h1 class="font-bold text-3xl mt-1">
                    Activity {{ route.params.id }}
                </h1>
                <p class="ml-3 text-muted flex items-center">
                    <Icon class="" name="ic:outline-access-time" />
                    <span class="ml-1">15 minutes</span>
                </p>
            </div>
            <p class="text-muted text-sm mt-2 mb-4">
                {{ faker.commerce.productDescription() }}
            </p>

            <slot></slot>
        </div>
    </article>
</template>
<script setup lang="ts">
import { faker } from "@faker-js/faker";

faker.seed(1);

const route = useRoute();
</script>
