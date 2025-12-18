"use client"

import { useAuth } from "@/components/auth-provider"
import { useRouter } from "next/navigation"
import { useEffect } from "react"
import Navbar from "@/components/navbar"
import GuidedTaleGenerator from "@/components/guided-tale-generator"
import { Loader2, Lock, Sparkles } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function GuidedTalePage() {
    const { user, loading } = useAuth()
    const router = useRouter()

    useEffect(() => {
        // Only redirect if we're done loading and there's no user
        if (!loading && !user) {
            router.push("/auth/login")
        }
    }, [user, loading, router])

    // Show loading state while checking authentication
    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
                <Navbar />
                <div className="flex items-center justify-center py-24">
                    <div className="text-center">
                        <Loader2 className="h-8 w-8 animate-spin text-purple-600 mx-auto mb-4" />
                        <p className="text-gray-600">Loading...</p>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
            <Navbar />
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">✨ Guided Story Creation</h1>
                    <p className="text-lg text-gray-600">Select your options and let the magic happen!</p>
                </div>

                {user ? (
                    <GuidedTaleGenerator />
                ) : (
                    <div className="text-center py-16">
                        <div className="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                            <Lock className="h-10 w-10 text-purple-600" />
                        </div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-4">Sign in to Create Stories</h2>
                        <p className="text-gray-600 mb-8 max-w-md mx-auto">
                            Join Cuentee to start creating personalized, magical stories for your family. It's free to get started!
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <Link href="/auth/sign-up">
                                <Button size="lg" className="bg-purple-600 hover:bg-purple-700">
                                    <Sparkles className="mr-2 h-4 w-4" />
                                    Get Started Free
                                </Button>
                            </Link>
                            <Link href="/auth/login">
                                <Button size="lg" variant="outline">
                                    Sign In
                                </Button>
                            </Link>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
