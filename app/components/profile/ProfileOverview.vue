<script setup lang="ts">
const props = defineProps<{
  user: {
    name: string
    email: string
    location?: string
    bio?: string
    streak: number
  }
}>()

defineEmits(["edit"])
</script>

<template>
  <div class="space-y-6">

    <!-- MAIN GRID -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">

      <!-- LEFT: PROFILE INFO -->
      <div>
        <h2 class="text-lg font-semibold text-green-700 mb-4">Profile Information</h2>

        <div class="space-y-4">

          <div>
            <p class="text-sm text-gray-500">Full name</p>
            <p class="font-medium">{{ user.name }}</p>
          </div>

          <div>
            <p class="text-sm text-gray-500">Username</p>
            <p class="font-medium">—</p>
          </div>

          <div>
            <p class="text-sm text-gray-500">Email</p>
            <p class="font-medium">{{ user.email }}</p>
          </div>

          <div v-if="user.location">
            <p class="text-sm text-gray-500">Location</p>
            <p class="font-medium">{{ user.location }}</p>
          </div>

          <div v-if="user.bio">
            <p class="text-sm text-gray-500">Bio</p>
            <p class="italic">"{{ user.bio }}"</p>
          </div>

        </div>
      </div>

      <!-- MIDDLE: STATISTICS -->
      <div>
        <h2 class="text-lg font-semibold text-green-700 mb-4">Statistics</h2>

        <div class="space-y-4">
          <div class="p-4 bg-gray-50 rounded-xl shadow-sm">
            <p class="text-sm text-gray-500">Programs enrolled</p>
            <p class="text-2xl font-bold text-green-700">0</p>
          </div>

          <div class="p-4 bg-gray-50 rounded-xl shadow-sm">
            <p class="text-sm text-gray-500">Current streak</p>
            <p class="text-2xl font-bold text-green-700">{{ user.streak }}</p>
          </div>

          <div class="p-4 bg-gray-50 rounded-xl shadow-sm">
            <p class="text-sm text-gray-500">Total time spent</p>
            <p class="text-2xl font-bold text-green-700">4h 20m</p>
          </div>
        </div>
      </div>

      <!-- RIGHT: ACHIEVEMENTS -->
      <div>
        <h2 class="text-lg font-semibold text-green-700 mb-4">Achievements</h2>

        <div class="space-y-3">
          <div class="flex items-center gap-3 bg-green-50 border border-green-200 rounded-xl p-3 shadow-sm">
            <span class="text-xl">🔥</span>
            <p>7-day streak</p>
          </div>

          <div class="flex items-center gap-3 bg-blue-50 border border-blue-200 rounded-xl p-3 shadow-sm">
            <span class="text-xl">⏱️</span>
            <p>100+ minutes trained</p>
          </div>

          <div class="flex items-center gap-3 bg-yellow-50 border border-yellow-200 rounded-xl p-3 shadow-sm">
            <span class="text-xl">🎯</span>
            <p>First activity completed</p>
          </div>

          <div class="flex items-center gap-3 bg-purple-50 border border-purple-200 rounded-xl p-3 shadow-sm">
            <span class="text-xl">📅</span>
            <p>Joined Salus</p>
          </div>

          <div class="flex items-center gap-3 bg-orange-50 border border-orange-200 rounded-xl p-3 shadow-sm">
            <span class="text-xl">🧘</span>
            <p>Meditation habit started</p>
          </div>
        </div>
      </div>

    </div>

    <!-- EDIT BUTTON -->
    <AppButton
      color="green"
      class="w-full"
      @click="$emit('edit')"
    >
      Edit Profile
    </AppButton>

  </div>
</template>