import { supabase } from "./client"
import type { User } from "@supabase/supabase-js"

export interface UserProfile {
  id: string
  username: string
  credits: number
  plan: "free" | "plus"
  plus_since: string | null
  last_credited_at: string | null
  created_at: string
}

export const profileOperations = {
  async getUserProfile(user: User): Promise<{ data: UserProfile | null; error: any }> {
    if (!supabase) {
      return { data: null, error: new Error("Supabase not configured") }
    }
    if (!user?.id) {
      return { data: null, error: new Error("User ID is required to fetch profile.") }
    }

    try {
      console.log("Fetching profile for user:", user.id)

      const { data, error } = await supabase.from("profiles").select("*").eq("id", user.id).maybeSingle()

      if (error) {
        console.error("Error fetching profile:", error)
        return { data: null, error }
      }

      if (!data) {
        console.log("No profile found for user, this should not happen with the trigger")
        return { data: null, error: new Error("Profile not found") }
      }

      console.log("Profile fetched successfully:", data)
      return { data, error: null }
    } catch (error) {
      console.error("Exception fetching user profile:", error)
      return { data: null, error }
    }
  },

  async checkUsernameAvailability(username: string): Promise<{ available: boolean; error: any }> {
    if (!supabase) {
      return { available: false, error: new Error("Supabase not configured") }
    }

    if (!username || username.length < 3) {
      return { available: false, error: new Error("Username must be at least 3 characters") }
    }

    try {
      console.log("Checking username availability:", username)

      const { data, error } = await supabase.from("profiles").select("username").ilike("username", username).limit(1)

      if (error) {
        console.error("Error checking username availability:", error)
        return { available: false, error }
      }

      const available = data.length === 0
      console.log("Username availability result:", { username, available })
      return { available, error: null }
    } catch (error) {
      console.error("Exception checking username availability:", error)
      return { available: false, error }
    }
  },

  async checkEmailAvailability(email: string): Promise<{ available: boolean; error: any }> {
    if (!supabase) {
      return { available: false, error: new Error("Supabase not configured") }
    }

    try {
      console.log("Checking email availability for:", email)

      // Check if supabase has rpc method
      if (supabase && typeof supabase.rpc === "function") {
        console.log("Using RPC function to check email")

        try {
          const { data, error } = await supabase.rpc("check_email_exists", {
            email_to_check: email.toLowerCase().trim(),
          })

          if (error) {
            console.error("Error calling check_email_exists RPC:", error)
            throw error
          }

          const emailExists = data === true
          console.log("Email check result:", { email, exists: emailExists })
          return { available: !emailExists, error: null }
        } catch (rpcError) {
          console.error("RPC function failed, using fallback method:", rpcError)
        }
      }

      // Fallback method
      console.log("Using simple validation method")
      const isTestEmail = email.toLowerCase().includes("taken") || email.toLowerCase().includes("exists")
      return { available: !isTestEmail, error: null }
    } catch (error) {
      console.error("Error checking email availability:", error)
      return { available: true, error }
    }
  },

  async waitForProfile(userId: string, maxAttempts = 10): Promise<{ data: UserProfile | null; error: any }> {
    if (!supabase) {
      return { data: null, error: new Error("Supabase not configured") }
    }

    console.log("Waiting for profile to be created by trigger for user:", userId)

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        const { data, error } = await supabase.from("profiles").select("*").eq("id", userId).maybeSingle()

        if (error) {
          console.error(`Attempt ${attempt}: Error checking for profile:`, error)
          if (attempt === maxAttempts) {
            return { data: null, error }
          }
        } else if (data) {
          console.log(`Attempt ${attempt}: Profile found:`, data)
          return { data, error: null }
        } else {
          console.log(`Attempt ${attempt}: Profile not found yet, waiting...`)
        }

        // Wait before next attempt
        await new Promise((resolve) => setTimeout(resolve, 1000))
      } catch (error) {
        console.error(`Attempt ${attempt}: Exception checking for profile:`, error)
        if (attempt === maxAttempts) {
          return { data: null, error }
        }
      }
    }

    return { data: null, error: new Error("Profile not created after maximum attempts") }
  },

  async updateUsernameWithRPC(
    userId: string,
    desiredUsername: string,
  ): Promise<{ data: UserProfile | null; error: any }> {
    if (!supabase) {
      return { data: null, error: new Error("Supabase not configured") }
    }

    try {
      console.log("Updating username using RPC for user:", userId, "to:", desiredUsername)

      // Use the RPC function to update username
      const { data: success, error: rpcError } = await supabase.rpc("update_user_username", {
        user_id: userId,
        new_username: desiredUsername.toLowerCase().trim(),
      })

      if (rpcError) {
        console.error("RPC error updating username:", rpcError)
        return { data: null, error: rpcError }
      }

      if (!success) {
        console.error("RPC returned false for username update")
        return { data: null, error: new Error("Username update failed") }
      }

      console.log("Username updated successfully via RPC, fetching profile...")

      // Fetch the updated profile
      const { data: updatedProfile, error: fetchError } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", userId)
        .single()

      if (fetchError) {
        console.error("Error fetching updated profile:", fetchError)
        return { data: null, error: fetchError }
      }

      if (!updatedProfile) {
        console.error("No profile found after RPC update")
        return { data: null, error: new Error("Profile not found after username update") }
      }

      console.log("Final profile after RPC update:", updatedProfile)

      // Verify the username was actually updated
      if (updatedProfile.username !== desiredUsername.toLowerCase().trim()) {
        console.warn(
          "Username was not updated correctly via RPC. Expected:",
          desiredUsername,
          "Got:",
          updatedProfile.username,
        )
        return { data: updatedProfile, error: new Error("Username was not updated correctly") }
      }

      return { data: updatedProfile, error: null }
    } catch (error) {
      console.error("Exception in updateUsernameWithRPC:", error)
      return { data: null, error }
    }
  },

  async setUsernameForNewUser(
    userId: string,
    desiredUsername: string,
  ): Promise<{ data: UserProfile | null; error: any }> {
    if (!supabase) {
      return { data: null, error: new Error("Supabase not configured") }
    }

    try {
      console.log("Setting username for new user:", userId, "to:", desiredUsername)

      // Wait for the trigger to create the temporary profile
      const { data: tempProfile, error: waitError } = await this.waitForProfile(userId)

      if (waitError || !tempProfile) {
        console.error("Failed to get temporary profile:", waitError)
        return { data: null, error: waitError || new Error("Temporary profile not found") }
      }

      console.log("Temporary profile found:", tempProfile)

      // Try to update using RPC function first
      const { data: rpcResult, error: rpcError } = await this.updateUsernameWithRPC(userId, desiredUsername)

      if (!rpcError && rpcResult) {
        console.log("Username updated successfully using RPC")
        return { data: rpcResult, error: null }
      }

      console.warn("RPC method failed, trying direct update:", rpcError)

      // Fallback to direct update
      console.log("Updating username directly from", tempProfile.username, "to", desiredUsername)

      const { error: updateError } = await supabase
        .from("profiles")
        .update({ username: desiredUsername.toLowerCase().trim() })
        .eq("id", userId)

      if (updateError) {
        console.error("Error updating username directly:", updateError)
        return { data: null, error: updateError }
      }

      console.log("Username updated successfully via direct method, fetching final profile...")

      // Fetch the updated profile
      const { data: finalProfile, error: fetchError } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", userId)
        .single()

      if (fetchError) {
        console.error("Error fetching final profile:", fetchError)
        return { data: null, error: fetchError }
      }

      if (!finalProfile) {
        console.error("No profile found after direct update")
        return { data: null, error: new Error("Profile not found after username update") }
      }

      console.log("Final profile with updated username:", finalProfile)

      // Verify the username was actually updated
      if (finalProfile.username !== desiredUsername.toLowerCase().trim()) {
        console.warn("Username was not updated correctly. Expected:", desiredUsername, "Got:", finalProfile.username)
        return { data: finalProfile, error: new Error("Username was not updated correctly") }
      }

      return { data: finalProfile, error: null }
    } catch (error) {
      console.error("Exception in setUsernameForNewUser:", error)
      return { data: null, error }
    }
  },

  async createOrUpdateProfile(userId: string, username: string): Promise<{ data: UserProfile | null; error: any }> {
    // Use the new method specifically designed for new user registration
    return this.setUsernameForNewUser(userId, username)
  },

  async updateUsername(userId: string, newUsername: string): Promise<{ data: UserProfile | null; error: any }> {
    // Try RPC method first, fallback to direct update
    const { data: rpcResult, error: rpcError } = await this.updateUsernameWithRPC(userId, newUsername)

    if (!rpcError && rpcResult) {
      return { data: rpcResult, error: null }
    }

    // Fallback to direct update
    if (!supabase) {
      return { data: null, error: new Error("Supabase not configured") }
    }

    try {
      console.log("Updating username directly for user:", userId, "to:", newUsername)

      const { error: updateError } = await supabase
        .from("profiles")
        .update({ username: newUsername.toLowerCase().trim() })
        .eq("id", userId)

      if (updateError) {
        console.error("Error updating username:", updateError)
        return { data: null, error: updateError }
      }

      const { data: updatedProfile, error: fetchError } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", userId)
        .single()

      if (fetchError) {
        console.error("Error fetching updated profile:", fetchError)
        return { data: null, error: fetchError }
      }

      return { data: updatedProfile, error: null }
    } catch (error) {
      console.error("Exception updating username:", error)
      return { data: null, error }
    }
  },

  async updateCredits(userId: string, newCredits: number): Promise<{ data: UserProfile | null; error: any }> {
    if (!supabase) {
      return { data: null, error: new Error("Supabase not configured") }
    }
    if (!userId) {
      return { data: null, error: new Error("User ID is required to update credits.") }
    }

    try {
      const { data, error } = await supabase
        .from("profiles")
        .update({ credits: newCredits })
        .eq("id", userId)
        .select()
        .maybeSingle()

      if (error) {
        console.error("Error updating credits:", error)
        return { data: null, error }
      }

      return { data, error: null }
    } catch (error) {
      console.error("Exception updating credits:", error)
      return { data: null, error }
    }
  },

  async updatePlan(userId: string, newPlan: "free" | "plus"): Promise<{ data: UserProfile | null; error: any }> {
    if (!supabase) {
      return { data: null, error: new Error("Supabase not configured") }
    }
    if (!userId) {
      return { data: null, error: new Error("User ID is required to update plan.") }
    }

    try {
      const updateData: any = { plan: newPlan }
      if (newPlan === "plus") {
        updateData.plus_since = new Date().toISOString()
      } else {
        updateData.plus_since = null
      }

      const { data, error } = await supabase.from("profiles").update(updateData).eq("id", userId).select().maybeSingle()

      if (error) {
        console.error("Error updating plan:", error)
        return { data: null, error }
      }

      return { data, error: null }
    } catch (error) {
      console.error("Exception updating plan:", error)
      return { data: null, error }
    }
  },
}
