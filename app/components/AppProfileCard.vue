<template>
  <Card class="p-6 w-[360px]">

    <div class="flex items-center gap-4 mb-6">
      <div
        class="w-14 h-14 rounded-full bg-primary-light flex items-center justify-center text-xl font-semibold text-green-900"
      >
        {{ initials }}
      </div>

      <div>
        <p class="text-lg font-semibold text-text">
          {{ username }}
        </p>
        <p class="text-sm text-gray-500">
          {{ email }}
        </p>
      </div>
    </div>

   
    <div class="border-t border-gray-200 my-4"></div>

    
    <div class="text-sm text-gray-600 space-y-2">
      <p><span class="font-medium">User ID:</span> {{ id }}</p>
    </div>

    
    <div class="mt-6">
      <slot />
    </div>
  </Card>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { Card } from "@/components/ui/card"

const props = defineProps<{
  id: number
  username?: string | null
  email?: string | null
}>()

const initials = computed(() =>
  props.username?.charAt(0)?.toUpperCase() ?? "?"
)
</script>