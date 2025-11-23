"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { Menu, X, BookOpen, LogOut, User } from "lucide-react"
import { useAuth } from "@/components/auth-provider"
import { supabase, isSupabaseConfigured } from "@/lib/supabase/client"
import { profileOperations, type UserProfile } from "@/lib/supabase/profile-operations"

export default function Navbar() {
  const { user, loading } = useAuth()
  const [isOpen, setIsOpen] = useState(false)
  const [isLoggingOut, setIsLoggingOut] = useState(false)
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null)
  const [profileLoading, setProfileLoading] = useState(false)

  useEffect(() => {
    if (user && !loading) {
      loadUserProfile()
    } else {
      setUserProfile(null)
    }
  }, [user, loading])

  const loadUserProfile = async () => {
    if (!user) return

    setProfileLoading(true)
    try {
      const { data, error } = await profileOperations.getUserProfile(user)
      if (error) {
        console.error("Error loading user profile:", error)
      } else {
        setUserProfile(data)
      }
    } catch (error) {
      console.error("Exception loading user profile:", error)
    } finally {
      setProfileLoading(false)
    }
  }

  const navigation = [
    { name: "Make a Tale", href: "/make-tale" },
    { name: "Gallery", href: "/gallery" },
    { name: "About Us", href: "/about" },
    { name: "Pricing", href: "/pricing" },
    { name: "FAQ", href: "/faq" },
  ]

  const handleSignOut = async () => {
    setIsLoggingOut(true)
    try {
      console.log("Attempting sign out...")
      console.log("isSupabaseConfigured:", isSupabaseConfigured)
      console.log("Supabase client available:", !!supabase)

      if (supabase && isSupabaseConfigured) {
        const { error } = await supabase.auth.signOut()
        if (error) {
          console.error("Supabase signout error:", error)
        } else {
          console.log("Supabase signout successful.")
        }
      } else {
        console.warn("Supabase not configured or client not available, performing client-side logout simulation.")
      }

      // Forzar una recarga completa de la página para limpiar todo el estado
      // El AuthProvider detectará el SIGNED_OUT y redirigirá a /auth/login
      window.location.href = "/"
    } catch (error) {
      console.error("Error signing out (catch block):", error)
      // Aún redirigir incluso si hay un error
      window.location.href = "/"
    } finally {
      setIsLoggingOut(false)
    }
  }

  // Show loading state
  if (loading) {
    return (
      <nav className="bg-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="flex items-center space-x-2">
                <BookOpen className="h-8 w-8 text-purple-600" />
                <span className="text-xl font-bold text-gray-900">Cuentee</span>
              </Link>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <div className="animate-pulse bg-gray-200 h-8 w-20 rounded"></div>
            </div>
          </div>
        </div>
      </nav>
    )
  }

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <BookOpen className="h-8 w-8 text-purple-600" />
              <span className="text-xl font-bold text-gray-900">Cuentee</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-gray-700 hover:text-purple-600 px-3 py-2 text-sm font-medium transition-colors"
              >
                {item.name}
              </Link>
            ))}

            {user ? (
              <div className="flex items-center space-x-4">
                <Link href="/account">
                  <button className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 hover:text-purple-600 transition-colors">
                    <User className="h-4 w-4" />
                    My Account
                  </button>
                </Link>
                <span className="text-sm text-gray-600">
                  Hello, {profileLoading ? "Loading..." : userProfile?.username || user.email?.split("@")[0] || "User"}
                </span>
                <button
                  onClick={handleSignOut}
                  className={`flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-sm font-medium transition-colors ${
                    isLoggingOut ? "bg-gray-100 text-gray-400 cursor-not-allowed" : "text-gray-700 hover:bg-gray-50"
                  }`}
                  disabled={isLoggingOut}
                >
                  <LogOut className="h-4 w-4" />
                  {isLoggingOut ? "Signing out..." : "Sign Out"}
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link href="/auth/login">
                  <button className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors">
                    Sign In
                  </button>
                </Link>
                <Link href="/auth/sign-up">
                  <button className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-md transition-colors">
                    Get Started
                  </button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 hover:text-purple-600 focus:outline-none focus:text-purple-600"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="text-gray-700 hover:text-purple-600 block px-3 py-2 text-base font-medium"
                  onClick={() => setIsOpen(false)}
                >
                  {item.name}
                </Link>
              ))}

              {user ? (
                <div className="pt-4 border-t">
                  <Link href="/account" className="block px-3 py-2" onClick={() => setIsOpen(false)}>
                    <button className="w-full flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 hover:text-purple-600 transition-colors">
                      <User className="h-4 w-4" />
                      My Account
                    </button>
                  </Link>
                  <div className="px-3 py-2 text-sm text-gray-600">
                    Hello,{" "}
                    {profileLoading ? "Loading..." : userProfile?.username || user.email?.split("@")[0] || "User"}
                  </div>
                  <div className="px-3">
                    <button
                      onClick={() => {
                        setIsOpen(false)
                        handleSignOut()
                      }}
                      className={`w-full flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-sm font-medium transition-colors ${
                        isLoggingOut ? "bg-gray-100 text-gray-400 cursor-not-allowed" : "text-gray-700 hover:bg-gray-50"
                      }`}
                      disabled={isLoggingOut}
                    >
                      <LogOut className="h-4 w-4" />
                      {isLoggingOut ? "Signing out..." : "Sign Out"}
                    </button>
                  </div>
                </div>
              ) : (
                <div className="pt-4 border-t space-y-2">
                  <Link href="/auth/login" className="block px-3" onClick={() => setIsOpen(false)}>
                    <button className="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors">
                      Sign In
                    </button>
                  </Link>
                  <Link href="/auth/sign-up" className="block px-3" onClick={() => setIsOpen(false)}>
                    <button className="w-full px-3 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-md transition-colors">
                      Get Started
                    </button>
                  </Link>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
