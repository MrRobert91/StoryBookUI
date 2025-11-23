"use client"

import { useSearchParams } from "next/navigation"
import Link from "next/link"
import { BookOpen, AlertCircle } from "lucide-react"

export default function AuthErrorPage() {
  const searchParams = useSearchParams()
  const message = searchParams.get("message") || "An authentication error occurred"

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-pink-50 px-4">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
          <div className="flex items-center justify-center space-x-2 mb-8">
            <BookOpen className="h-8 w-8 text-purple-600" />
            <span className="text-2xl font-bold text-gray-900">Cuentee</span>
          </div>

          <div className="mb-6">
            <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Authentication Error</h1>
            <p className="text-gray-600 mb-4">{message}</p>
            <p className="text-sm text-gray-500">If you continue to experience issues, please contact support.</p>
          </div>

          <div className="space-y-3">
            <Link
              href="/auth/login"
              className="inline-block w-full px-6 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors"
            >
              Try Signing In
            </Link>
            <Link
              href="/"
              className="inline-block w-full px-6 py-3 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
            >
              Go to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
