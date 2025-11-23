"use client"

import { useEffect, useState } from "react"
import { useAuth } from "@/components/auth-provider"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { BookOpen, CheckCircle, Loader2 } from "lucide-react"

export default function ConfirmedPage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [redirecting, setRedirecting] = useState(false)

  useEffect(() => {
    if (!loading && user) {
      // User is confirmed and logged in, redirect to dashboard after a short delay
      setRedirecting(true)
      const timer = setTimeout(() => {
        router.push("/")
      }, 3000)

      return () => clearTimeout(timer)
    }
  }, [user, loading, router])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-pink-50">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-purple-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-pink-50 px-4">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
          <div className="flex items-center justify-center space-x-2 mb-8">
            <BookOpen className="h-8 w-8 text-purple-600" />
            <span className="text-2xl font-bold text-gray-900">Cuentee</span>
          </div>

          <div className="mb-6">
            <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Email Confirmed!</h1>
            <p className="text-gray-600">
              Your email has been successfully confirmed. You can now access all features of Cuentee.
            </p>
          </div>

          {user ? (
            <div className="space-y-4">
              <p className="text-sm text-gray-600">
                Welcome, {user.email}! {redirecting ? "Redirecting to your dashboard..." : ""}
              </p>
              {redirecting ? (
                <div className="flex items-center justify-center">
                  <Loader2 className="h-4 w-4 animate-spin text-purple-600 mr-2" />
                  <span className="text-sm text-gray-600">Redirecting...</span>
                </div>
              ) : (
                <Link
                  href="/"
                  className="inline-block w-full px-6 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors"
                >
                  Go to Dashboard
                </Link>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              <p className="text-sm text-gray-600">Please sign in to continue.</p>
              <Link
                href="/auth/login"
                className="inline-block w-full px-6 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors"
              >
                Sign In
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
