"use client"

import { useState, useEffect, useRef } from "react"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Sparkles, Loader2, BookOpen, Zap, AlertCircle, Check, Lock } from "lucide-react"
import StoryViewer from "./story-viewer"
import { storyOperations } from "@/lib/supabase/stories"
import { supabase, isSupabaseConfigured } from "@/lib/supabase/client"
import { useAuth } from "@/components/auth-provider"
import StripeModal from "./stripe-modal"
import { useStoryGeneration } from "@/hooks/use-story-generation"

interface Chapter {
  title: string
  content: string
  image_url?: string
}

export default function TaleGenerator() {
  const { user, loading: authLoading } = useAuth()
  const {
    isGenerating: isGeneratingAsync,
    status: asyncStatus,
    storyData: asyncStoryData,
    error: asyncError,
    generateStoryAsync,
    generateStory,
  } = useStoryGeneration()

  const [prompt, setPrompt] = useState("")
  const [story, setStory] = useState("")
  const [aiStory, setAiStory] = useState<Chapter[] | null>(null)
  const [storyTitle, setStoryTitle] = useState<string | null>(null)

  const [isGeneratingAI, setIsGeneratingAI] = useState(false)
  const [isGeneratingAIJWT, setIsGeneratingAIJWT] = useState(false)
  const [isGeneratingAIJWTImages, setIsGeneratingAIJWTImages] = useState(false)

  const [apiError, setApiError] = useState<string | null>(null)
  const [isSaving, setIsSaving] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)
  const [showNoCreditsModal, setShowNoCreditsModal] = useState(false)

  const asyncStorySavedRef = useRef(false)

  const fastApiUrl = process.env.NEXT_PUBLIC_FASTAPI_URL

  const resetStoryStates = () => {
    setStory("")
    setAiStory(null)
    setStoryTitle(null)
    setApiError(null)
    setSaveSuccess(false)
    setSaveError(null)
    setShowNoCreditsModal(false)
  }

  const generateAIStory = async () => {
    if (!prompt.trim()) return
    if (!user) {
      setApiError("You must be logged in to use 'Generate Story (AI)'.")
      return
    }

    resetStoryStates()
    setIsGeneratingAI(true)

    try {
      if (!fastApiUrl) {
        console.warn("NEXT_PUBLIC_FASTAPI_URL not set, using demo data for AI endpoint.")
        throw new Error("API URL not configured for AI endpoint.")
      }

      const API_URL = `${fastApiUrl}/generate-story-ai`
      console.log("Making request to AI endpoint:", API_URL)

      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: prompt.trim() }),
      })

      if (!response.ok) {
        const errorText = await response.text()
        console.error("API Error Response (AI):", errorText)
        throw new Error(`API Error: ${response.status} - ${response.statusText}`)
      }

      const data = await response.json()
      if (data.chapters && Array.isArray(data.chapters)) {
        setAiStory(data.chapters)
        setStoryTitle(data.title || null)
        if (user?.id) {
          const storyTitle = data.title || "AI Generated Tale"
          saveStoryToDatabase(user.id, storyTitle, data, prompt)
        }
      } else {
        throw new Error("Invalid response format from AI API")
      }
    } catch (error) {
      console.error("Error generating AI story:", error)
      setApiError(error instanceof Error ? error.message : "Unknown error occurred")
      console.log("Using demo data as fallback for AI story")
      const demoChapters: Chapter[] = [
        {
          title: "The Beginning of Adventure (AI Fallback)",
          content: `In a land where dreams take flight and magic flows like rivers, our story begins with ${prompt}. 
The morning sun painted the sky in shades of gold and pink as our brave protagonist discovered something extraordinary that would change their life forever.
Little did they know, this was just the beginning of the most incredible adventure they would ever experienced.`,
        },
        {
          title: "The Mysterious Discovery (AI Fallback)",
          content: `As they ventured deeper into the enchanted realm, strange and wonderful things began to happen. The very air seemed to shimmer with possibility.
Ancient trees whispered secrets in languages long forgotten, and magical creatures peeked out from behind glowing mushrooms, curious about this new visitor to their world.
Something important was about to be revealed - something that would test their courage and determination.`,
        },
      ]
      setAiStory(demoChapters)
      setStoryTitle("AI Generated Tale (Fallback)")
      if (user?.id) {
        saveStoryToDatabase(
          user.id,
          "AI Generated Tale (Fallback)",
          { chapters: demoChapters, title: "AI Generated Tale (Fallback)" },
          prompt,
        )
      }
    } finally {
      setIsGeneratingAI(false)
    }
  }

  const generateStoryWithAIJWT = async () => {
    if (!prompt.trim()) return
    if (!user) {
      setApiError("You must be logged in to use 'Generate Story (AI with JWT)'.")
      return
    }

    resetStoryStates()
    setIsGeneratingAIJWT(true)

    try {
      if (!isSupabaseConfigured || !supabase) {
        throw new Error("Supabase is not configured.")
      }

      const {
        data: { session },
        error: sessionError,
      } = await supabase.auth.getSession()

      if (sessionError || !session?.access_token) {
        console.error("Session error or missing access token:", sessionError, session)
        throw new Error("Authentication required. Please log in again.")
      }

      if (!fastApiUrl) {
        console.warn("NEXT_PUBLIC_FASTAPI_URL not set, using demo data for JWT endpoint.")
        throw new Error("API URL not configured for JWT endpoint.")
      }

      const API_URL = `${fastApiUrl}/generate-story-ai-jwt`
      console.log("Making request to AI JWT endpoint:", API_URL)

      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.access_token}`,
        },
        body: JSON.stringify({ prompt: prompt.trim() }),
      })

      if (response.status === 401) {
        throw new Error("Authentication failed. Please log in again.")
      }

      if (response.status === 402) {
        setShowNoCreditsModal(true)
        throw new Error("No te quedan créditos disponibles. Suscríbete para seguir generando historias.")
      }

      if (!response.ok) {
        const errorText = await response.text()
        console.error("API Error Response (AI JWT):", errorText)
        throw new Error(`API Error: ${response.status} - ${response.statusText}`)
      }

      const data = await response.json()
      if (data.chapters && Array.isArray(data.chapters)) {
        setAiStory(data.chapters)
        setStoryTitle(data.title || null)
        if (user?.id) {
          const storyTitle = data.title || "AI Generated Tale (JWT)"
          saveStoryToDatabase(user.id, storyTitle, data, prompt)
        }
      } else {
        console.error("Invalid response format:", data)
        throw new Error("Invalid response format from AI JWT API")
      }
    } catch (error) {
      console.error("Error generating AI story with JWT:", error)
      if (error instanceof Error) {
        setApiError(error.message)
      } else {
        setApiError("Unknown error occurred")
      }

      if (!showNoCreditsModal) {
        console.log("Using demo data as fallback for AI JWT story")
        const demoChapters: Chapter[] = [
          {
            title: "The Beginning of Adventure (JWT Fallback)",
            content: `In a land where dreams take flight and magic flows like rivers, our story begins with ${prompt}. 
The morning sun painted the sky in shades of gold and pink as our brave protagonist discovered something extraordinary that would change their life forever.`,
          },
          {
            title: "The Mysterious Discovery (JWT Fallback)",
            content: `As they ventured deeper into the enchanted realm, strange and wonderful things began to happen. The very air seemed to shimmer with possibility.
Ancient trees whispered secrets in languages long forgotten, and magical creatures peeked out from behind glowing mushrooms.`,
          },
        ]
        setAiStory(demoChapters)
        setStoryTitle("AI Generated Tale (JWT Fallback)")
        if (user?.id) {
          saveStoryToDatabase(
            user.id,
            "AI Generated Tale (JWT Fallback)",
            { chapters: demoChapters, title: "AI Generated Tale (JWT Fallback)" },
            prompt,
          )
        }
      }
    } finally {
      setIsGeneratingAIJWT(false)
    }
  }

  const generateStoryWithImagesAIJWT = async () => {
    if (!prompt.trim()) return
    if (!user) {
      setApiError("You must be logged in to use 'Generate Story with Images (AI with JWT)'.")
      return
    }

    resetStoryStates()
    setIsGeneratingAIJWTImages(true)

    try {
      if (!isSupabaseConfigured || !supabase) {
        throw new Error("Supabase is not configured.")
      }

      const {
        data: { session },
        error: sessionError,
      } = await supabase.auth.getSession()

      if (sessionError || !session?.access_token) {
        throw new Error("Authentication required. Please log in again.")
      }

      if (!fastApiUrl) {
        console.warn("NEXT_PUBLIC_FASTAPI_URL not set, using demo data for image JWT endpoint.")
        throw new Error("API URL not configured for image JWT endpoint.")
      }

      const API_URL = `${fastApiUrl}/generate-story-ai-images-jwt`
      console.log("[v0] Making request to AI Images JWT endpoint:", API_URL)
      console.log("[v0] Prompt:", prompt.trim())
      console.log("[v0] Auth token present:", !!session.access_token)

      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.access_token}`,
        },
        body: JSON.stringify({ prompt: prompt.trim() }),
      })

      console.log("[v0] Response status:", response.status)
      console.log("[v0] Response headers:", Object.fromEntries(response.headers.entries()))

      if (response.status === 401) {
        throw new Error("Authentication failed. Please log in again.")
      }

      if (response.status === 402) {
        setShowNoCreditsModal(true)
        throw new Error("No te quedan créditos disponibles. Suscríbete para seguir generando historias.")
      }

      if (!response.ok) {
        const errorText = await response.text()
        console.error("[v0] API Error Response (AI Images JWT):", errorText)
        console.error("[v0] Response status:", response.status)
        console.error("[v0] Response statusText:", response.statusText)
        throw new Error(`API Error: ${response.status} - ${response.statusText}`)
      }

      const data = await response.json()
      console.log("[v0] Response data:", data)

      if (!data) {
        throw new Error("Empty response from API")
      }

      if (data.chapters && Array.isArray(data.chapters)) {
        console.log("[v0] Valid chapters found:", data.chapters.length)
        setAiStory(data.chapters)
        setStoryTitle(data.title || null)
        if (user?.id) {
          const storyTitle = data.title || "AI Generated Tale with Images (JWT)"
          saveStoryToDatabase(user.id, storyTitle, data, prompt)
        }
      } else {
        console.error("[v0] Invalid response format:", data)
        throw new Error("Invalid response format from AI Images JWT API - missing or invalid chapters")
      }
    } catch (error) {
      console.error("[v0] Error generating AI story with images:", error)
      if (error instanceof Error) {
        setApiError(error.message)
      } else {
        setApiError("Unknown error occurred")
      }

      if (!showNoCreditsModal) {
        console.log("[v0] Using demo data as fallback for AI Images JWT story")
        const demoChapters: Chapter[] = [
          {
            title: "The Beginning of Adventure (Images Fallback)",
            content: `https://images.unsplash.com/photo-1614613535308-eb5fbd8952e7?w=600&h=400&fit=crop\n\nIn a land where dreams take flight and magic flows like rivers, our story begins with ${prompt}. 
The morning sun painted the sky in shades of gold and pink as our brave protagonist discovered something extraordinary that would change their life forever.`,
          },
          {
            title: "The Mysterious Discovery (Images Fallback)",
            content: `https://images.unsplash.com/photo-1516979187457-635ffe35c91c?w=600&h=400&fit=crop\n\nAs they ventured deeper into the enchanted realm, strange and wonderful things began to happen. The very air seemed to shimmer with possibility.
Ancient trees whispered secrets in languages long forgotten, and magical creatures peeked out from behind glowing mushrooms.`,
          },
        ]
        setAiStory(demoChapters)
        setStoryTitle("AI Generated Tale with Images (Fallback)")
        if (user?.id) {
          saveStoryToDatabase(
            user.id,
            "AI Generated Tale with Images (Fallback)",
            { chapters: demoChapters, title: "AI Generated Tale with Images (Fallback)" },
            prompt,
          )
        }
      }
    } finally {
      setIsGeneratingAIJWTImages(false)
    }
  }

  const saveStoryToDatabase = async (
    userId: string,
    title: string,
    content: string | Chapter[] | Record<string, any>,
    originalPrompt: string,
  ) => {
    setIsSaving(true)
    setSaveError(null)
    setSaveSuccess(false)

    try {
      const { data, error } = await storyOperations.saveStory(userId, title, content, originalPrompt)

      if (error) {
        console.error("Save story error:", error)
        throw error
      }

      setSaveSuccess(true)
      setTimeout(() => setSaveSuccess(false), 3000)
    } catch (error) {
      console.error("Error saving story:", error)
      setSaveError(error instanceof Error ? error.message : "Failed to save story")
      setTimeout(() => setSaveError(null), 5000)
    } finally {
      setIsSaving(false)
    }
  }

  useEffect(() => {
    if (asyncStoryData && asyncStoryData.chapters && Array.isArray(asyncStoryData.chapters)) {
      if (!asyncStorySavedRef.current) {
        console.log("[v0] Async story completed:", asyncStoryData)
        setAiStory(asyncStoryData.chapters)
        setStoryTitle(asyncStoryData.title || "AI Generated Tale with Images Async")

        asyncStorySavedRef.current = true
      }
    }
  }, [asyncStoryData])

  useEffect(() => {
    if (asyncError) {
      setApiError(asyncError)
    }
  }, [asyncError])

  const handleGenerateStoryAsync = async () => {
    if (!prompt.trim()) return
    if (!user) {
      setApiError("You must be logged in to use 'Generate Story with Images Async'.")
      return
    }

    resetStoryStates()
    asyncStorySavedRef.current = false

    try {
      if (!isSupabaseConfigured || !supabase) {
        throw new Error("Supabase is not configured.")
      }

      const {
        data: { session },
        error: sessionError,
      } = await supabase.auth.getSession()

      if (sessionError || !session?.access_token) {
        throw new Error("Authentication required. Please log in again.")
      }

      await generateStory(prompt.trim(), "dall-e-3", session.access_token)
    } catch (error) {
      console.error("[v0] Error initiating async story generation:", error)
      if (error instanceof Error) {
        setApiError(error.message)
      } else {
        setApiError("Unknown error occurred")
      }
    }
  }

  const isAnyGenerating = isGeneratingAI || isGeneratingAIJWT || isGeneratingAIJWTImages || isGeneratingAsync

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 p-4 sm:p-6 lg:p-8">
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-purple-600" />
              Story Prompt
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Textarea
              placeholder="Describe your story idea... For example: 'A brave princess who befriends a friendly dragon and goes on an adventure to save her village from a magical storm'"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={4}
              className="resize-none"
              disabled={isAnyGenerating || authLoading}
            />

            {(isSaving || saveSuccess || saveError) && (
              <div
                className={`text-sm p-3 rounded-lg flex items-center gap-2 ${
                  saveSuccess
                    ? "bg-green-50 text-green-700 border border-green-200"
                    : saveError
                      ? "bg-red-50 text-red-700 border border-red-200"
                      : "bg-blue-50 text-blue-700 border border-blue-200"
                }`}
              >
                {isSaving && <Loader2 className="h-4 w-4 animate-spin" />}
                {saveSuccess && <Check className="h-4 w-4" />}
                {saveError && <AlertCircle className="h-4 w-4" />}
                <span>
                  {isSaving && "Saving story..."}
                  {saveSuccess && "Story saved successfully!"}
                  {saveError && `Save error: ${saveError}`}
                </span>
              </div>
            )}

            <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${fastApiUrl ? "bg-green-500" : "bg-yellow-500"}`}></div>
                <span>API Status: {fastApiUrl ? "Configured" : "Using Demo Mode"}</span>
              </div>
            </div>

            {apiError && (
              <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-lg">
                <div className="flex items-center gap-2">
                  <AlertCircle className="h-4 w-4" />
                  <span className="font-medium">API Error:</span>
                </div>
                <p className="text-sm mt-1">{apiError}</p>
              </div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <button
                onClick={generateAIStory}
                className={`py-4 px-6 text-lg font-medium rounded-lg transition-colors flex items-center justify-center ${
                  !prompt.trim() || isAnyGenerating || authLoading || !user
                    ? "bg-gray-400 cursor-not-allowed text-gray-600"
                    : "bg-pink-600 hover:bg-pink-700 text-white"
                }`}
                disabled={!prompt.trim() || isAnyGenerating || authLoading || !user}
              >
                {isGeneratingAI ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating AI...
                  </>
                ) : (
                  <>
                    <Zap className="mr-2 h-4 w-4" />
                    Generate Story (AI)
                  </>
                )}
              </button>

              <button
                onClick={generateStoryWithAIJWT}
                className={`py-4 px-6 text-lg font-medium rounded-lg transition-colors flex items-center justify-center ${
                  !prompt.trim() || isAnyGenerating || authLoading || !user
                    ? "bg-gray-400 cursor-not-allowed text-gray-600"
                    : "bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white"
                }`}
                disabled={!prompt.trim() || isAnyGenerating || authLoading || !user}
              >
                {isGeneratingAIJWT ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating AI (JWT)...
                  </>
                ) : (
                  <>
                    <Zap className="mr-2 h-4 w-4" />
                    Generate Story (AI with JWT)
                  </>
                )}
              </button>

              <button
                onClick={generateStoryWithImagesAIJWT}
                className={`py-4 px-6 text-lg font-medium rounded-lg transition-colors flex items-center justify-center sm:col-span-2 ${
                  !prompt.trim() || isAnyGenerating || authLoading || !user
                    ? "bg-gray-400 cursor-not-allowed text-gray-600"
                    : "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white"
                }`}
                disabled={!prompt.trim() || isAnyGenerating || authLoading || !user}
              >
                {isGeneratingAIJWTImages ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating with Images...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Generate Story with Images (AI with JWT)
                  </>
                )}
              </button>

              <button
                onClick={handleGenerateStoryAsync}
                disabled={isAnyGenerating || !prompt.trim()}
                className="sm:col-span-2 w-full bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold py-3 px-6 rounded-lg transition duration-200 disabled:cursor-not-allowed"
              >
                {isGeneratingAsync ? (
                  <>
                    <span className="inline-block animate-spin mr-2">⚙️</span>
                    Generating... ({asyncStatus})
                  </>
                ) : (
                  "Generate Story with Images Async"
                )}
              </button>
            </div>

            {isGeneratingAsync && (
              <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-blue-800 text-sm">Status: {asyncStatus}</p>
              </div>
            )}

            {asyncError && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-800 text-sm">{asyncError}</p>
              </div>
            )}

            {!user && (
              <div className="text-center text-sm text-gray-600 mt-4 flex items-center justify-center gap-2">
                <Lock className="h-4 w-4 text-gray-500" />
                Sign in to use "Generate Story (AI)" and "Generate Story (AI with JWT)" and save your tales.
              </div>
            )}
          </CardContent>
        </Card>

        {aiStory && <StoryViewer chapters={aiStory} title={storyTitle || undefined} />}

        {story && !aiStory && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-green-600" />
                Your Magical Tale
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose prose-lg max-w-none">
                <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border-l-4 border-purple-500">
                  <p className="whitespace-pre-line text-gray-800 leading-relaxed">{story}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        <StripeModal isOpen={showNoCreditsModal} onClose={() => setShowNoCreditsModal(false)} />
      </div>
    </div>
  )
}
