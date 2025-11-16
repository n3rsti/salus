<script setup lang="ts">
defineProps({
  emoji: { type: String, required: true },
  label: { type: String, required: true },
  color: { type: String, default: "green" }
});
</script>

<template>
  <div
    class="flex items-center gap-2 px-3 py-2 rounded-lg border text-sm font-medium"
    :class="{
      'bg-green-50  border-green-200 text-gray-800': color === 'green',
      'bg-blue-50   border-blue-200 text-gray-800': color === 'blue',
      'bg-yellow-50 border-yellow-200 text-gray-800': color === 'yellow',
      'bg-orange-50 border-orange-200 text-gray-800': color === 'orange',
      'bg-purple-50 border-purple-200 text-gray-800': color === 'purple'
    }"
  >
    <span class="text-xl">{{ emoji }}</span>
    <span>{{ label }}</span>
  </div>
</template>