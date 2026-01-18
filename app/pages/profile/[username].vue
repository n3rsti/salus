<script setup lang="ts">
import { ref, onMounted } from "vue";

definePageMeta({
  public: true,
});

const route = useRoute();
const username = route.params.username as string;

const user = ref<{
  username: string;
  programs: any[];
  activities: any[];
} | null>(null);

const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
  try {
    const [programs, activities] = await Promise.all([
      $fetch<any[]>("/api/programs"),
      $fetch<any[]>("/api/activities"),
    ]);

    const createdPrograms = programs.filter(
      (p) => p.owner?.username === username
    );

    const createdActivities = activities.filter(
      (a) => a.owner?.username === username
    );

    user.value = {
      username,
      programs: createdPrograms,
      activities: createdActivities,
    };
  } catch (e) {
    console.error(e);
    error.value = "Failed to load public profile.";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="space-y-6">
    
    <Card class="p-6">
      <h1 class="text-xl font-semibold text-green-600">
        {{ username }}
      </h1>
    </Card>

    <Card v-if="loading" class="p-6 text-gray-500">
      Loading profile…
    </Card>

    <Card v-else-if="error" class="p-6 text-red-500">
      {{ error }}
    </Card>

    <template v-else>

      <Card class="p-6">
        <h2 class="text-lg font-semibold mb-2">Created programs</h2>

        <p v-if="!user?.programs.length" class="text-gray-500">
          No programs yet.
        </p>

        <ul v-else class="list-disc pl-5 space-y-1">
          <li v-for="program in user.programs" :key="program.id">
            {{ program.name }}
          </li>
        </ul>
      </Card>

      
      <Card class="p-6">
        <h2 class="text-lg font-semibold mb-2">Created activities</h2>

        <p v-if="!user?.activities.length" class="text-gray-500">
          No activities yet.
        </p>

        <ul v-else class="list-disc pl-5 space-y-1">
          <li v-for="activity in user.activities" :key="activity.id">
            {{ activity.name }}
          </li>
        </ul>
      </Card>
    </template>
  </div>
</template>