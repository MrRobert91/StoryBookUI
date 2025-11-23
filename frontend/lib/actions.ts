"use server"

import { createClient } from "@/lib/supabase/server"
import { redirect } from "next/navigation"

// Update the signIn function to handle redirects properly
export async function signIn(prevState: any, formData: FormData) {
  try {
    // Check if formData is valid
    if (!formData) {
      console.error("Form data is missing")
      return { error: "Form data is missing" }
    }

    const email = formData.get("email")
    const password = formData.get("password")

    // Validate required fields
    if (!email || !password) {
      console.error("Email or password missing")
      return { error: "Email and password are required" }
    }

    console.log("Attempting to sign in with email:", email)

    const supabase = await createClient()

    const { data, error } = await supabase.auth.signInWithPassword({
      email: email.toString(),
      password: password.toString(),
    })

    if (error) {
      console.error("Supabase auth error:", error)
      return { error: error.message }
    }

    if (data.user) {
      console.log("Login successful for user:", data.user.email)
      return { success: true }
    }

    return { error: "Login failed - no user returned" }
  } catch (error) {
    console.error("Login error:", error)
    return { error: "An unexpected error occurred. Please try again." }
  }
}

// Update the signUp function to handle potential null formData
export async function signUp(prevState: any, formData: FormData) {
  try {
    // Check if formData is valid
    if (!formData) {
      console.error("Form data is missing")
      return { error: "Form data is missing" }
    }

    const email = formData.get("email")
    const password = formData.get("password")

    // Validate required fields
    if (!email || !password) {
      console.error("Email or password missing")
      return { error: "Email and password are required" }
    }

    console.log("Attempting to sign up with email:", email)

    const supabase = await createClient()

    const { data, error } = await supabase.auth.signUp({
      email: email.toString(),
      password: password.toString(),
    })

    if (error) {
      console.error("Supabase signup error:", error)
      return { error: error.message }
    }

    if (data.user) {
      console.log("Signup successful for user:", data.user.email)
      return { success: "Check your email to confirm your account." }
    }

    return { error: "Signup failed - no user returned" }
  } catch (error) {
    console.error("Sign up error:", error)
    return { error: "An unexpected error occurred. Please try again." }
  }
}

// Simplified signOut function - no longer used since we're doing client-side logout
export async function signOut() {
  try {
    const supabase = await createClient()

    const { error } = await supabase.auth.signOut()

    if (error) {
      console.error("Sign out error:", error)
    }
  } catch (error) {
    console.error("Sign out error:", error)
  }

  redirect("/auth/login")
}
