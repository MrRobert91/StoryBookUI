"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Loader2, Check, X } from "lucide-react"
import Link from "next/link"
import { supabase, isSupabaseConfigured } from "@/lib/supabase/client"
import { profileOperations } from "@/lib/supabase/profile-operations"

export default function SignUpForm() {
  const [email, setEmail] = useState("")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState<{ type: "error" | "success"; text: string } | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const [emailStatus, setEmailStatus] = useState<{
    checking: boolean
    available: boolean | null
    error: string | null
    validFormat: boolean
  }>({
    checking: false,
    available: null,
    error: null,
    validFormat: false,
  })

  const [usernameStatus, setUsernameStatus] = useState<{
    checking: boolean
    available: boolean | null
    error: string | null
  }>({
    checking: false,
    available: null,
    error: null,
  })

  // Email validation regex
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  // Username validation regex
  const usernameRegex = /^[a-z0-9_.]{3,20}$/
  const invalidPatternRegex = /^[._]|[._]$|[._]{2,}/

  // Email validation and availability check
  useEffect(() => {
    if (!email) {
      setEmailStatus({ checking: false, available: null, error: null, validFormat: false })
      return
    }

    // Check format first
    const isValidFormat = emailRegex.test(email)

    if (!isValidFormat) {
      setEmailStatus({
        checking: false,
        available: false,
        error: "Please enter a valid email address",
        validFormat: false,
      })
      return
    }

    // If format is valid, check availability
    const timeoutId = setTimeout(async () => {
      setEmailStatus((prev) => ({ ...prev, checking: true, validFormat: true }))

      try {
        const { available, error } = await profileOperations.checkEmailAvailability(email)

        if (error) {
          console.error("Email availability check error:", error)
          setEmailStatus({
            checking: false,
            available: false,
            error: "Error checking email availability. Please try again.",
            validFormat: true,
          })
        } else {
          setEmailStatus({
            checking: false,
            available,
            error: available ? null : "This email is already registered",
            validFormat: true,
          })
        }
      } catch (error) {
        console.error("Email availability check exception:", error)
        setEmailStatus({
          checking: false,
          available: false,
          error: "Error checking email availability. Please try again.",
          validFormat: true,
        })
      }
    }, 500)

    return () => clearTimeout(timeoutId)
  }, [email])

  // Username validation and availability check
  useEffect(() => {
    if (!username || username.length < 3) {
      setUsernameStatus({ checking: false, available: null, error: null })
      return
    }

    // Validate format first
    if (!usernameRegex.test(username)) {
      setUsernameStatus({
        checking: false,
        available: false,
        error: "Username must be 3-20 characters, lowercase letters, numbers, dots and underscores only",
      })
      return
    }

    if (invalidPatternRegex.test(username)) {
      setUsernameStatus({
        checking: false,
        available: false,
        error: "Username cannot start/end with . or _ or have consecutive . or _",
      })
      return
    }

    const timeoutId = setTimeout(async () => {
      setUsernameStatus({ checking: true, available: null, error: null })

      try {
        const { available, error } = await profileOperations.checkUsernameAvailability(username)

        if (error) {
          setUsernameStatus({
            checking: false,
            available: false,
            error: "Error checking username availability",
          })
        } else {
          setUsernameStatus({
            checking: false,
            available,
            error: available ? null : "Username is already taken",
          })
        }
      } catch (error) {
        setUsernameStatus({
          checking: false,
          available: false,
          error: "Error checking username availability",
        })
      }
    }, 500)

    return () => clearTimeout(timeoutId)
  }, [username])

  // Check if form is valid and ready to submit
  const isFormValid =
    email &&
    username &&
    password &&
    password.length >= 6 &&
    emailStatus.validFormat &&
    emailStatus.available === true &&
    usernameStatus.available === true &&
    !emailStatus.checking &&
    !usernameStatus.checking

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!isFormValid) {
      setMessage({ type: "error", text: "Please fix all validation errors before submitting" })
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

      console.log("Starting signup process for:", email, "with username:", username)

      // Create the auth user - the trigger will automatically create a temporary profile
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email: email.trim(),
        password: password,
      })

      console.log("Signup result:", { authData, authError })

      if (authError) {
        console.error("Supabase signup error:", authError)

        // Handle specific error types
        if (
          authError.message.includes("User already registered") ||
          authError.message.includes("already been registered")
        ) {
          setMessage({ type: "error", text: "An account with this email already exists. Please sign in instead." })
          setEmailStatus((prev) => ({ ...prev, available: false, error: "Email is already registered" }))
        } else if (authError.message.includes("Password should be")) {
          setMessage({ type: "error", text: "Password is too weak. Please choose a stronger password." })
        } else if (authError.message.includes("Database error")) {
          setMessage({
            type: "error",
            text: "There was a database error. This might be a temporary issue. Please try again in a few moments.",
          })
        } else {
          setMessage({ type: "error", text: authError.message })
        }
        return
      }

      if (authData.user) {
        console.log("User created successfully, now setting up profile with username:", username)

        try {
          // Use the improved method to set the username for the new user
          const { data: profileData, error: profileError } = await profileOperations.setUsernameForNewUser(
            authData.user.id,
            username.toLowerCase(),
          )

          if (profileError) {
            console.error("Profile setup error:", profileError)

            // Handle specific errors
            if (profileError.code === "23505" || profileError.message.includes("duplicate key")) {
              setMessage({ type: "error", text: "Username is not available. Please choose another one." })
              setUsernameStatus((prev) => ({ ...prev, available: false, error: "Username is already taken" }))
              return
            } else if (profileError.message.includes("Username was not updated correctly")) {
              setMessage({
                type: "success",
                text: `Account created successfully! However, there was an issue setting your username. You can update it in your profile after logging in. Please check your email to confirm your account.`,
              })
            } else {
              // Even if profile setup has issues, the user account was created successfully
              console.warn("Profile setup had issues but user account exists:", profileError)
              setMessage({
                type: "success",
                text: "Account created successfully! Please check your email to confirm your account. You can update your username in your profile if needed.",
              })
            }
          } else if (profileData) {
            console.log("Signup and profile setup successful:", { user: authData.user.email, profile: profileData })

            // Verify the username was set correctly
            if (profileData.username === username.toLowerCase()) {
              setMessage({
                type: "success",
                text: `Account created successfully with username "${profileData.username}"! Please check your email to confirm your account.`,
              })
            } else {
              setMessage({
                type: "success",
                text: `Account created successfully! Your username was set to "${profileData.username}". Please check your email to confirm your account.`,
              })
            }
          } else {
            // Fallback success message
            setMessage({
              type: "success",
              text: "Account created successfully! Please check your email to confirm your account.",
            })
          }
        } catch (profileException) {
          console.error("Profile setup exception:", profileException)
          setMessage({
            type: "success",
            text: "Account created successfully! Please check your email to confirm your account. You can set up your profile after logging in.",
          })
        }

        // Clear form regardless of profile setup result
        setEmail("")
        setUsername("")
        setPassword("")
        setEmailStatus({ checking: false, available: null, error: null, validFormat: false })
        setUsernameStatus({ checking: false, available: null, error: null })
      } else {
        setMessage({ type: "error", text: "Signup failed. Please try again." })
      }
    } catch (error) {
      console.error("Signup error:", error)

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
        <h1 className="text-3xl font-semibold tracking-tight text-gray-900">Create an account</h1>
        <p className="text-gray-600">Sign up to start creating magical stories for your family</p>
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
            <div className="relative">
              <input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={`w-full px-3 py-2 pr-10 bg-white border rounded-md text-gray-900 placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:border-transparent ${emailStatus.error
                    ? "border-red-300 focus:ring-red-500"
                    : emailStatus.available === true
                      ? "border-green-300 focus:ring-green-500"
                      : "border-gray-300 focus:ring-purple-500"
                  }`}
                disabled={isLoading}
                required
              />
              <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                {emailStatus.checking ? (
                  <Loader2 className="h-4 w-4 animate-spin text-gray-400" />
                ) : emailStatus.available === true ? (
                  <Check className="h-4 w-4 text-green-500" />
                ) : emailStatus.available === false ? (
                  <X className="h-4 w-4 text-red-500" />
                ) : null}
              </div>
            </div>
            <div className="text-xs space-y-1">
              {emailStatus.error && <p className="text-red-600">{emailStatus.error}</p>}
              {emailStatus.available === true && <p className="text-green-600">Email is available!</p>}
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="username" className="block text-sm font-medium text-gray-700">
              Username
            </label>
            <div className="relative">
              <input
                id="username"
                type="text"
                placeholder="your_username"
                value={username}
                onChange={(e) => setUsername(e.target.value.toLowerCase())}
                className={`w-full px-3 py-2 pr-10 bg-white border rounded-md text-gray-900 placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:border-transparent ${usernameStatus.error
                    ? "border-red-300 focus:ring-red-500"
                    : usernameStatus.available === true
                      ? "border-green-300 focus:ring-green-500"
                      : "border-gray-300 focus:ring-purple-500"
                  }`}
                disabled={isLoading}
                required
              />
              <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                {usernameStatus.checking ? (
                  <Loader2 className="h-4 w-4 animate-spin text-gray-400" />
                ) : usernameStatus.available === true ? (
                  <Check className="h-4 w-4 text-green-500" />
                ) : usernameStatus.available === false ? (
                  <X className="h-4 w-4 text-red-500" />
                ) : null}
              </div>
            </div>
            <div className="text-xs space-y-1">
              <p className="text-gray-500">3-20 characters, lowercase letters, numbers, dots and underscores only</p>
              {usernameStatus.error && <p className="text-red-600">{usernameStatus.error}</p>}
              {usernameStatus.available === true && <p className="text-green-600">Username is available!</p>}
            </div>
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
              className={`w-full px-3 py-2 bg-white border rounded-md text-gray-900 focus:outline-none focus:ring-2 focus:border-transparent ${password && password.length < 6
                  ? "border-red-300 focus:ring-red-500"
                  : password && password.length >= 6
                    ? "border-green-300 focus:ring-green-500"
                    : "border-gray-300 focus:ring-purple-500"
                }`}
              disabled={isLoading}
              required
            />
            <div className="text-xs space-y-1">
              <p className="text-gray-500">Password must be at least 6 characters long</p>
              {password && password.length < 6 && <p className="text-red-600">Password is too short</p>}
              {password && password.length >= 6 && <p className="text-green-600">Password length is valid</p>}
            </div>
          </div>

          <button
            type="submit"
            disabled={!isFormValid || isLoading}
            className={`w-full py-6 text-lg font-medium rounded-lg h-[60px] transition-colors ${!isFormValid || isLoading
                ? "bg-gray-400 cursor-not-allowed text-gray-600"
                : "bg-[#2b725e] hover:bg-[#235e4c] text-white"
              }`}
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Creating account...
              </span>
            ) : (
              "Create Account"
            )}
          </button>

          {/* Form validation status indicator */}
          {!isFormValid && (email || username || password) && (
            <div className="text-xs text-gray-600 bg-gray-50 p-3 rounded-lg">
              <p className="font-medium mb-2">Please complete the following:</p>
              <ul className="space-y-1">
                {!emailStatus.validFormat && email && (
                  <li className="flex items-center text-red-600">
                    <X className="h-3 w-3 mr-1" />
                    Valid email format
                  </li>
                )}
                {emailStatus.validFormat && emailStatus.available !== true && (
                  <li className="flex items-center text-red-600">
                    <X className="h-3 w-3 mr-1" />
                    Email must be available
                  </li>
                )}
                {emailStatus.available === true && (
                  <li className="flex items-center text-green-600">
                    <Check className="h-3 w-3 mr-1" />
                    Email is valid and available
                  </li>
                )}

                {usernameStatus.available !== true && username && (
                  <li className="flex items-center text-red-600">
                    <X className="h-3 w-3 mr-1" />
                    Username must be valid and available
                  </li>
                )}
                {usernameStatus.available === true && (
                  <li className="flex items-center text-green-600">
                    <Check className="h-3 w-3 mr-1" />
                    Username is valid and available
                  </li>
                )}

                {password && password.length < 6 && (
                  <li className="flex items-center text-red-600">
                    <X className="h-3 w-3 mr-1" />
                    Password must be at least 6 characters
                  </li>
                )}
                {password && password.length >= 6 && (
                  <li className="flex items-center text-green-600">
                    <Check className="h-3 w-3 mr-1" />
                    Password meets requirements
                  </li>
                )}
              </ul>
            </div>
          )}
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
              console.error("Google signup error:", error)
              setMessage({ type: "error", text: "Failed to sign up with Google" })
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
          Sign up with Google
        </button>

        <div className="text-center text-gray-600">
          Already have an account?{" "}
          <Link href="/auth/login" className="text-purple-600 hover:text-purple-700 font-medium">
            Log in
          </Link>
        </div>
      </div>
    </div>
  )
}
