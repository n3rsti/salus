<script setup lang="ts">
const { name, avatar, location } = defineProps<{
  name: string
  avatar: string
  location?: string
}>()
</script>

<template>
  <div class="flex items-center gap-4">
    <img
      :src="avatar"
      alt="avatar"
      class="w-20 h-20 rounded-full object-cover"
    />

    <div>
      <p class="text-xl font-semibold">{{ name }}</p>

      <p class="text-gray-500 text-sm">
        {{ location || "Unknown location" }}
      </p>
    </div>
  </div>
</template>