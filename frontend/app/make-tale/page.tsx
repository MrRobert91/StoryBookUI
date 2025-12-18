"use client"

import { useAuth } from "@/components/auth-provider"
import { useRouter } from "next/navigation"
import { useEffect } from "react"
import Navbar from "@/components/navbar"
import { Button } from "@/components/ui/button"
import { Sparkles, BookOpen, Compass, Lock, Loader2 } from "lucide-react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"

export default function MakeTalePage() {
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
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">✨ Create Your Magical Tale</h1>
                    <p className="text-lg text-gray-600">Choose how you want to create your story today!</p>
                </div>

                {user ? (
                    <div className="grid md:grid-cols-2 gap-8">
                        <Card className="hover:shadow-lg transition-shadow border-purple-200">
                            <CardHeader className="text-center">
                                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <BookOpen className="h-8 w-8 text-purple-600" />
                                </div>
                                <CardTitle className="text-xl">Open Story</CardTitle>
                                <CardDescription>
                                    Unleash your imagination! Write a prompt and let AI weave a unique tale from scratch.
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="text-center">
                                <p className="text-sm text-muted-foreground mb-4">
                                    Perfect for those who have a specific idea in mind.
                                </p>
                            </CardContent>
                            <CardFooter className="flex justify-center pb-8">
                                <Link href="/make-tale/open">
                                    <Button size="lg" className="bg-purple-600 hover:bg-purple-700">
                                        Create Open Story
                                    </Button>
                                </Link>
                            </CardFooter>
                        </Card>

                        <Card className="hover:shadow-lg transition-shadow border-teal-200">
                            <CardHeader className="text-center">
                                <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <Compass className="h-8 w-8 text-teal-600" />
                                </div>
                                <CardTitle className="text-xl">Guided Story</CardTitle>
                                <CardDescription>
                                    Follow a magical path! Select key elements like age, theme, and mission to build your story step-by-step.
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="text-center">
                                <p className="text-sm text-muted-foreground mb-4">
                                    Great for structured storytelling and educational themes.
                                </p>
                            </CardContent>
                            <CardFooter className="flex justify-center pb-8">
                                <Link href="/make-tale/guided">
                                    <Button size="lg" className="bg-teal-600 hover:bg-teal-700">
                                        Create Guided Story
                                    </Button>
                                </Link>
                            </CardFooter>
                        </Card>
                    </div>
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
