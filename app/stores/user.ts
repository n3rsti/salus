
import { defineStore } from "pinia"

export const useUserStore = defineStore("user", {
  state: () => ({
    id: null as number | null,
    username: null as string | null,
    email: null as string | null,
  }),

  actions: {
    async fetchUser(userId: number) {
      const res = await fetch(`http://localhost:8000/api/users/${userId}`, {
        credentials: "include",
      })

      if (!res.ok) {
        throw new Error("Failed to fetch user")
      }

      const data = await res.json()

      this.id = data.id
      this.username = data.username
      this.email = data.email
    },
  },

  persist: true,
})
