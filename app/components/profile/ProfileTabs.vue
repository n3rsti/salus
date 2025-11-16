<script setup lang="ts">
const props = defineProps<{
  active: string
}>()

const emit = defineEmits(["update:active"])

const tabs = [
  { id: "overview", label: "Overview" },
  { id: "activity", label: "Activity" },
  { id: "settings", label: "Settings" }
]

const setTab = (id: string) => emit("update:active", id)
</script>

<template>
  <div class="flex flex-col gap-3 w-full">

    <button
      v-for="t in tabs"
      :key="t.id"
      @click="setTab(t.id)"
      class="rounded-xl px-4 py-3 text-left font-medium transition-all border shadow-sm"
      :class="props.active === t.id
        ? 'bg-green-600 text-white border-green-600 shadow'
        : 'bg-white border-gray-200 text-green-700 hover:bg-green-50 hover:border-green-600'"
    >
      {{ t.label }}
    </button>

  </div>
</template>