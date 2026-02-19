"use client"

import { useState, useEffect, useRef } from "react"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Sparkles, Loader2, AlertCircle, Check, Lock, Mic, MicOff } from "lucide-react"
import StoryViewer from "./story-viewer"
import { supabase, isSupabaseConfigured } from "@/lib/supabase/client"
import { useAuth } from "@/components/auth-provider"
import StripeModal from "./stripe-modal"
import { useStoryGeneration } from "@/hooks/use-story-generation"
import { useLanguage } from "./language-context"

interface Chapter {
  title: string
  content: string
  image_url?: string
}

export default function TaleGenerator() {
  const STOP_RECORDING_DELAY_MS = 1000

  const { user, loading: authLoading } = useAuth()
  const { language, t } = useLanguage()
  const {
    isGenerating: isGeneratingAsync,
    status: asyncStatus,
    storyData: asyncStoryData,
    error: asyncError,
    generateStory,
  } = useStoryGeneration()

  const [prompt, setPrompt] = useState("")
  const [aiStory, setAiStory] = useState<Chapter[] | null>(null)
  const [storyTitle, setStoryTitle] = useState<string | null>(null)
  const [numChapters, setNumChapters] = useState("3")
  const [visualStyle, setVisualStyle] = useState("cartoons")

  const [apiError, setApiError] = useState<string | null>(null)
  const [isSaving, setIsSaving] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)
  const [showNoCreditsModal, setShowNoCreditsModal] = useState(false)

  // Recording states
  const [isRecording, setIsRecording] = useState(false)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const socketRef = useRef<WebSocket | null>(null)
  const stopTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const isStoppingRecordingRef = useRef(false)

  const asyncStorySavedRef = useRef(false)

  const fastApiUrl = process.env.NEXT_PUBLIC_FASTAPI_URL || "http://localhost:8000"

  const resetStoryStates = () => {
    setAiStory(null)
    setStoryTitle(null)
    setApiError(null)
    setSaveSuccess(false)
    setSaveError(null)
    setShowNoCreditsModal(false)
  }

  const appendText = (text: string) => {
    setPrompt((prev) => {
      const prefix = prev.trim().length > 0 ? " " : ""
      return prev + prefix + text
    })
  }

  const toggleRecording = async () => {
    if (isRecording) {
      await stopRecording()
    } else {
      await startRecording()
    }
  }

  const startRecording = async () => {
    try {
      if (isStoppingRecordingRef.current) {
        return
      }

      if (isRecording) {
        return
      }

      if (!user) {
        setApiError("Authentication required for voice input.")
        return
      }

      // Check for session to get token
      const { data: { session } } = await supabase.auth.getSession()
      if (!session?.access_token) {
        setApiError("Session expired. Please log in again.")
        return
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

      // Determine WebSocket URL (handling http/https vs ws/wss)
      const wsProtocol = fastApiUrl.startsWith("https") ? "wss" : "ws"
      const wsHost = fastApiUrl.replace(/^https?:\/\//, "")
      const wsUrl = `${wsProtocol}://${wsHost}/transcription/transcribe?token=${session.access_token}&lang=${encodeURIComponent(language)}`

      console.log("Connecting to WS:", wsUrl) // Debug log
      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        console.log("WebSocket Connected")
        const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })

        recorder.ondataavailable = (event) => {
          if (event.data.size > 0 && ws.readyState === WebSocket.OPEN) {
            ws.send(event.data)
          }
        }

        recorder.start(250) // Send chunks every 250ms
        mediaRecorderRef.current = recorder
        setIsRecording(true)
        setApiError(null)
      }

      ws.onmessage = (event) => {
        try {
          const response = JSON.parse(event.data)
          if (response.type === 'final') {
            appendText(response.text)
          }
          // Currently ignoring partials to avoid janky text updates, 
          // can enable later if we add a 'preview' text area.
        } catch (e) {
          console.error("Error parsing WS message", e)
        }
      }

      ws.onerror = (e) => {
        console.error("WebSocket error:", e)
        setApiError("Error connecting to transcription service.")
        void stopRecording(false)
      }

      ws.onclose = () => {
        console.log("WebSocket Disconnected")
        socketRef.current = null
      }

      socketRef.current = ws
    } catch (err) {
      console.error("Error accessing microphone:", err)
      setApiError("Could not access microphone. Please check permissions.")
      setIsRecording(false)
    }
  }

  const finalizeStopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop()
      mediaRecorderRef.current.stream.getTracks().forEach((track) => track.stop())
    }

    if (socketRef.current) {
      // Avoid calling close if already closed to prevent errors
      if (socketRef.current.readyState === WebSocket.OPEN || socketRef.current.readyState === WebSocket.CONNECTING) {
        socketRef.current.close()
      }
    }

    mediaRecorderRef.current = null
    socketRef.current = null
  }

  const stopRecording = async (withDelay = true) => {
    // Visual feedback should stop immediately
    setIsRecording(false)

    if (stopTimeoutRef.current) {
      clearTimeout(stopTimeoutRef.current)
      stopTimeoutRef.current = null
    }

    const hasActiveRecorder = !!mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive"
    const hasOpenSocket =
      !!socketRef.current &&
      (socketRef.current.readyState === WebSocket.OPEN || socketRef.current.readyState === WebSocket.CONNECTING)

    if (!hasActiveRecorder && !hasOpenSocket) {
      isStoppingRecordingRef.current = false
      return
    }

    if (!withDelay) {
      isStoppingRecordingRef.current = false
      finalizeStopRecording()
      return
    }

    isStoppingRecordingRef.current = true

    await new Promise<void>((resolve) => {
      stopTimeoutRef.current = setTimeout(() => {
        finalizeStopRecording()
        isStoppingRecordingRef.current = false
        stopTimeoutRef.current = null
        resolve()
      }, STOP_RECORDING_DELAY_MS)
    })
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      void stopRecording(false)
    }
  }, [])

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
      if (asyncError.includes("créditos") || asyncError.includes("402")) {
        setShowNoCreditsModal(true)
      }
    }
  }, [asyncError])

  const handleGenerateStoryAsync = async () => {
    if (isRecording || isStoppingRecordingRef.current) {
      await stopRecording(true)
    }

    if (!prompt.trim()) return
    if (!user) {
      setApiError("You must be logged in to generate stories.")
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

      await generateStory({
        topic: prompt.trim(),
        num_chapters: parseInt(numChapters),
        visual_style: visualStyle,
        lang: language
      }, session.access_token)
    } catch (error) {
      console.error("[v0] Error initiating async story generation:", error)
      if (error instanceof Error) {
        setApiError(error.message)
      } else {
        setApiError("Unknown error occurred")
      }
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 p-4 sm:p-6 lg:p-8">
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-purple-600" />
              {t("tale_generator.story_prompt")}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">


            <div className="relative">
              <Textarea
                placeholder={t("tale_generator.prompt_placeholder")}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                rows={4}
                className="resize-none pr-12"
                disabled={isGeneratingAsync || authLoading}
              />
              <button
                onClick={toggleRecording}
                className={`absolute bottom-3 right-3 p-2 rounded-full transition-all duration-200 shadow-sm ${isRecording
                    ? "bg-red-100 text-red-600 hover:bg-red-200 animate-pulse ring-2 ring-red-400"
                    : "bg-gray-100 text-gray-500 hover:bg-gray-200 hover:text-purple-600"
                  }`}
                title={isRecording ? t("tale_generator.stop_voice") : t("tale_generator.start_voice")}
                type="button"
                disabled={isGeneratingAsync || authLoading}
              >
                {isRecording ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
              </button>
            </div>

            {/* Chapter Length Selector */}
            <div className="space-y-2">
              <span className="text-sm font-medium text-gray-700">{t("tale_generator.story_length")}</span>
              <div className="flex gap-4">
                {["3", "6", "9"].map((num) => (
                  <label key={num} className="flex items-center gap-2 cursor-pointer bg-white px-3 py-2 rounded-md border hover:bg-gray-50 transition-colors">
                    <input
                      type="radio"
                      name="numChapters"
                      value={num}
                      checked={numChapters === num}
                      onChange={(e) => setNumChapters(e.target.value)}
                      className="w-4 h-4 text-purple-600 focus:ring-purple-500"
                      disabled={isGeneratingAsync}
                    />
                    <span className="text-sm text-gray-700">
                      {num === "3" ? t("tale_generator.short") : num === "6" ? t("tale_generator.medium") : t("tale_generator.long")}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            {/* Visual Style Selector */}
            <div className="space-y-3">
              <span className="text-sm font-medium text-gray-700">{t("tale_generator.art_style")}</span>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
                {[
                  { id: "cartoons", label: "Cartoons", icon: "🎨" },
                  { id: "watercolor", label: "Watercolor", icon: "🖌️" },
                  { id: "3d_animation", label: "3D Animation", icon: "🎭" },
                  { id: "anime", label: "Anime", icon: "🏯" },
                  { id: "child_crayons", label: "Child's Drawing", icon: "🖍️" },
                ].map((style) => (
                  <div
                    key={style.id}
                    onClick={() => !isGeneratingAsync && setVisualStyle(style.id)}
                    className={`
                      cursor-pointer rounded-lg border p-3 flex flex-col items-center justify-center gap-2 transition-all
                      ${visualStyle === style.id
                        ? "bg-purple-50 border-purple-500 ring-1 ring-purple-500 text-purple-700"
                        : "bg-white border-gray-200 hover:border-purple-300 hover:bg-gray-50 text-gray-600"}
                      ${isGeneratingAsync ? "opacity-50 cursor-not-allowed" : ""}
                    `}
                  >
                    <span className="text-2xl">{style.icon}</span>
                    <span className="text-xs font-medium text-center">{t(`styles.${style.id}`)}</span>
                  </div>
                ))}
              </div>
            </div>

            {(isSaving || saveSuccess || saveError) && (
              <div
                className={`text-sm p-3 rounded-lg flex items-center gap-2 ${saveSuccess
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
                  {isSaving && t("tale_generator.saving")}
                  {saveSuccess && t("tale_generator.save_success")}
                  {saveError && `${t("tale_generator.save_error")}: ${saveError}`}
                </span>
              </div>
            )}

            {apiError && (
              <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-lg">
                <div className="flex items-center gap-2">
                  <AlertCircle className="h-4 w-4" />
                  <span className="font-medium">Error:</span>
                </div>
                <p className="text-sm mt-1">{apiError}</p>
              </div>
            )}

            <button
              onClick={handleGenerateStoryAsync}
              disabled={isGeneratingAsync || !prompt.trim() || authLoading || !user}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold py-4 px-6 rounded-lg transition duration-200 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isGeneratingAsync ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  {t("tale_generator.generating")} ({asyncStatus})
                </>
              ) : (
                <>
                  <Sparkles className="h-5 w-5" />
                  {t("tale_generator.generate_button")}
                </>
              )}
            </button>

            {isGeneratingAsync && (
              <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-blue-800 text-sm">{t("tale_generator.status")}: {asyncStatus}</p>
              </div>
            )}

            {!user && (
              <div className="text-center text-sm text-gray-600 mt-4 flex items-center justify-center gap-2">
                <Lock className="h-4 w-4 text-gray-500" />
                {t("tale_generator.sign_in_to_generate")}
              </div>
            )}
          </CardContent>
        </Card>

        {aiStory && <StoryViewer chapters={aiStory} title={storyTitle || undefined} />}

        <StripeModal isOpen={showNoCreditsModal} onClose={() => setShowNoCreditsModal(false)} />
      </div>
    </div>
  )
}

