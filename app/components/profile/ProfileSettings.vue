<script setup lang="ts">
const props = defineProps<{
  user: {
    name: string
    email: string
    location?: string
    bio?: string
  }
}>()
</script>

<template>
  <AppCard>
    <h2 class="text-lg font-semibold text-green-700 mb-4">
      Edit Profile
    </h2>

    <div class="space-y-5">

      <!-- DISPLAY NAME -->
      <div>
        <label class="block text-gray-600 mb-1">Display name</label>
        <input
          type="text"
          class="w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-green-600 outline-none"
          :placeholder="props.user.name"
        />
      </div>

      <!-- LOCATION -->
      <div>
        <label class="block text-gray-600 mb-1">Location</label>
        <input
          type="text"
          class="w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-green-600 outline-none"
          :placeholder="props.user.location || 'Enter location'"
        />
      </div>

      <!-- BIO -->
      <div>
        <label class="block text-gray-600 mb-1">Bio</label>
        <textarea
          rows="3"
          class="w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-green-600 outline-none"
          :placeholder="props.user.bio || 'Say something about yourself...'"
        ></textarea>
      </div>

      <!-- BUTTON -->
      <AppButton class="w-full" color="green_dark">
        Save Changes
      </AppButton>
    </div>
  </AppCard>
</template>