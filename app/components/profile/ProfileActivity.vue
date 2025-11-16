<script setup lang="ts">
import AppActivityCard from "~/components/AppActivityCard.vue"

const activities = [
  {
    id: 1,
    name: "Morning Meditation",
    duration_minutes: 10,
    description: "Start your day with calm focus.",
    difficulty: 1,
    rating: 4,
    image_url: "null"
  },
  {
    id: 2,
    name: "Cold Shower",
    duration_minutes: 3,
    description: "Boost your energy and alertness.",
    difficulty: 3,
    rating: 5,
    image_url: " "
  }
]
</script>

<template>
  <div class="grid gap-4">
    <AppActivityCard
      v-for="a in activities"
      :key="a.id"
      :activity="a"
      buttonColor="green"
    />
  </div>
</template>

