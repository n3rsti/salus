<script setup lang="ts">
import { ref } from "vue";

import ProfileOverview from "~/components/profile/ProfileOverview.vue";
import ProfileActivity from "~/components/profile/ProfileActivity.vue";
import ProfileSettings from "~/components/profile/ProfileSettings.vue";

const active = ref("overview");

// MOCK USER
const user = {
  name: "name surname",
  email: "name@example.com",
  location: "Zagreb, Croatia",
  bio: "Trying to improve every day",
  streak: 7
};

// MOCK ACTIVITIES
const activities = [
  { id: 1, name: "Morning Meditation", duration_minutes: 10 },
  { id: 2, name: "Cold Shower", duration_minutes: 3 }
];

const tabs = [
  { id: "overview", label: "Overview" },
  { id: "activity", label: "Activity" },
  { id: "settings", label: "Settings" }
];

function goToSettings() {
  active.value = "settings";
}
</script>

<template>
  <div class="w-full">

    
    <h2 class="text-xl font-semibold text-green-700 mb-4">
      Profile
    </h2>

    
    <div class="flex gap-3 mb-8">
      <button
        v-for="t in tabs"
        :key="t.id"
        @click="active = t.id"
        class="px-4 py-2 rounded-md font-medium transition-all border outline-none"
        :class="active === t.id
          ? 'border-green-700 text-green-700 bg-white'
          : 'border-gray-200 text-gray-600 hover:bg-[#EBFCEB] hover:text-green-700'"
      >
        {{ t.label }}
      </button>
    </div>

    
    <ProfileOverview
      v-if="active === 'overview'"
      :user="user"
      @edit="goToSettings"
    />

    <ProfileActivity
      v-if="active === 'activity'"
      :activities="activities"
    />

    <ProfileSettings
      v-if="active === 'settings'"
      :user="user"
    />

  </div>
</template>