"use client"

import type React from "react"

import { useState } from "react"
import { Loader2 } from "lucide-react"
import Link from "next/link"
import { supabase, isSupabaseConfigured } from "@/lib/supabase/client"
import { useRouter } from "next/navigation" // Importar useRouter

export default function LoginForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState<{ type: "error" | "success"; text: string } | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter() // Inicializar useRouter

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!email || !password) {
      setMessage({ type: "error", text: "Email and password are required" })
      return
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      setMessage({ type: "error", text: "Please enter a valid email address" })
      return
    }

    setIsLoading(true)
    setMessage(null)

    try {
      if (!isSupabaseConfigured) {
        setMessage({ type: "error", text: "Authentication service is not configured. Please contact support." })
        return
      }

      if (!supabase || !supabase.auth) {
        setMessage({ type: "error", text: "Authentication service is not available. Please try again later." })
        return
      }

      const { data, error } = await supabase.auth.signInWithPassword({
        email: email.trim(),
        password: password,
      })

      if (error) {
        console.error("Supabase auth error:", error)

        // Handle specific error types
        if (error.message.includes("Invalid login credentials")) {
          setMessage({ type: "error", text: "Invalid email or password. Please check your credentials and try again." })
        } else if (error.message.includes("Email not confirmed")) {
          setMessage({ type: "error", text: "Please check your email and confirm your account before signing in." })
        } else if (error.message.includes("Too many requests")) {
          setMessage({ type: "error", text: "Too many login attempts. Please wait a moment and try again." })
        } else {
          setMessage({ type: "error", text: error.message })
        }
      } else if (data.user) {
        console.log("Login successful for user:", data.user.email)
        setMessage({ type: "success", text: "Login successful! Redirecting..." })

        // Clear form
        setEmail("")
        setPassword("")

        // Redirigir a la página principal después de un login exitoso
        router.push("/")
      } else {
        setMessage({ type: "error", text: "Login failed. Please try again." })
      }
    } catch (error) {
      console.error("Login error:", error)

      if (error instanceof TypeError && error.message.includes("Failed to fetch")) {
        setMessage({
          type: "error",
          text: "Network error. Please check your internet connection and try again.",
        })
      } else {
        setMessage({ type: "error", text: "An unexpected error occurred. Please try again." })
      }
    } finally {
      setIsLoading(false)
    }
  }

  // Show configuration warning if Supabase is not configured
  if (!isSupabaseConfigured) {
    return (
      <div className="w-full space-y-8">
        <div className="space-y-2 text-center">
          <h1 className="text-3xl font-semibold tracking-tight text-gray-900">Authentication Setup Required</h1>
          <p className="text-gray-600">Supabase authentication is not configured</p>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-lg">
          <h3 className="font-medium">Configuration Missing</h3>
          <p className="text-sm mt-1">Please configure your Supabase environment variables:</p>
          <ul className="text-xs mt-2 list-disc list-inside">
            <li>NEXT_PUBLIC_SUPABASE_URL</li>
            <li>NEXT_PUBLIC_SUPABASE_ANON_KEY</li>
          </ul>
        </div>

        <div className="text-center">
          <Link href="/" className="text-purple-600 hover:text-purple-700 font-medium">
            ← Back to Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="w-full space-y-8">
      <div className="space-y-2 text-center">
        <h1 className="text-3xl font-semibold tracking-tight text-gray-900">Welcome back</h1>
        <p className="text-gray-600">Sign in to your account to continue creating magical stories</p>
      </div>

      <div className="space-y-6">
        {message && (
          <div
            className={`px-4 py-3 rounded-lg ${message.type === "error"
                ? "bg-red-50 border border-red-200 text-red-700"
                : "bg-green-50 border border-green-200 text-green-700"
              }`}
          >
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-gray-900 placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              disabled={isLoading}
              required
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              disabled={isLoading}
              required
            />
          </div>

          <button
            type="submit"
            disabled={isLoading || !email || !password}
            className={`w-full py-6 text-lg font-medium rounded-lg h-[60px] transition-colors ${isLoading || !email || !password
                ? "bg-gray-400 cursor-not-allowed text-gray-600"
                : "bg-[#2b725e] hover:bg-[#235e4c] text-white"
              }`}
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Signing in...
              </span>
            ) : (
              "Sign In"
            )}
          </button>
        </form>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-[#fcfaf8] px-2 text-gray-500">Or continue with</span>
          </div>
        </div>

        <button
          type="button"
          onClick={async () => {
            setIsLoading(true)
            try {
              const { error } = await supabase.auth.signInWithOAuth({
                provider: "google",
                options: {
                  redirectTo: `${window.location.origin}/api/auth/callback`,
                },
              })
              if (error) throw error
            } catch (error) {
              console.error("Google login error:", error)
              setMessage({ type: "error", text: "Failed to sign in with Google" })
              setIsLoading(false)
            }
          }}
          disabled={isLoading}
          className="w-full py-3 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-gray-700 font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors flex items-center justify-center h-[60px]"
        >
          {isLoading ? (
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24">
              <path
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                fill="#4285F4"
              />
              <path
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                fill="#34A853"
              />
              <path
                d="M5.84 14.17c-.22-.66-.35-1.36-.35-2.17s.13-1.51.35-2.17V7.01H2.18C.79 9.78.79 14.22 2.18 16.99l3.66-2.82z"
                fill="#FBBC05"
              />
              <path
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.01l3.66 2.82c.87-2.6 3.3-4.45 6.16-4.45z"
                fill="#EA4335"
              />
            </svg>
          )}
          Sign in with Google
        </button>

        <div className="text-center text-gray-600">
          Don't have an account?{" "}
          <Link href="/auth/sign-up" className="text-purple-600 hover:text-purple-700 font-medium">
            Sign up
          </Link>
        </div>
      </div>
    </div>
  )
}
