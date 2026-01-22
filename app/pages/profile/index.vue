<template>
  <div class="space-y-6">
    
    <Card class="p-6">
      <h1 class="text-xl font-semibold text-green-600">Profile</h1>
    </Card>

    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      <Card class="p-6 space-y-4">
        <h2 class="text-lg font-semibold">User information</h2>

        <div class="space-y-3 text-sm">
          <div>
            <label class="block text-gray-500 mb-1">Username</label>
            <div class="input bg-gray-50">
              {{ displayUser.username }}
            </div>
          </div>

          <div>
            <label class="block text-gray-500 mb-1">Email</label>
            <div class="input bg-gray-50">
              {{ displayUser.email ?? "-" }}
            </div>
          </div>

          <div>
            <label class="block text-gray-500 mb-1">User ID</label>
            <div class="input bg-gray-50">
              {{ displayUser.id }}
            </div>
          </div>
        </div>
      </Card>

      
      <Card class="p-6 space-y-4">
        <h2 class="text-lg font-semibold">Edit username</h2>

        <div class="space-y-3">
          <label class="block text-gray-500 text-sm">New username</label>
          <input
            v-model="newUsername"
            class="input bg-white text-black border border-gray-300 focus:border-green-500 focus:ring-1 focus:ring-green-500"
            placeholder="Enter new username"
    >
        </div>

        <Button
          variant="success"
          :disabled="isSaving || !newUsername"
          @click="saveUsername"
        >
          {{ isSaving ? "Saving..." : "Save changes" }}
        </Button>

        <p v-if="success" class="text-green-600 text-sm">
          Username updated successfully
        </p>
        <p v-if="error" class="text-red-600 text-sm">
          {{ error }}
        </p>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"


interface User {
  id: number
  username: string | null
  email: string | null
}

const userStore = useUserStore()
const isLoading = ref(true)
onMounted(async () => {
  if (userStore.id && userStore.id !== 0) {
    await userStore.fetchUser(userStore.id)
  }
  isLoading.value = false
})


const mockUser: User = {
  id: 1,
  username: "mock_user",
  email: "mock_user@test.com",
}


const displayUser = computed<User>(() => {
  if (userStore.id && userStore.id !== 0) {
    return {
      id: userStore.id,
      username: userStore.username,
      email: userStore.email,
    }
  }
  return mockUser
})


const newUsername = ref("")
const isSaving = ref(false)
const error = ref("")
const success = ref(false)

const saveUsername = async () => {
  error.value = ""
  success.value = false
  isSaving.value = true

  try {
    
    const updatedUser = await $fetch<User>(
      `/api/users/${displayUser.value.id}`,
      {
        method: "PUT",
        body: {
          username: newUsername.value,
        },
      }
    )

    userStore.username = updatedUser.username
    success.value = true
  } catch (e: any) {
    error.value = e?.data?.detail || "Failed to update username"
  } finally {
    isSaving.value = false
  }
}
</script>

