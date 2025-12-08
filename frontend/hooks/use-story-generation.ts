"use client"

import { useState, useCallback, useRef, useEffect } from "react"

export type StoryStatus = "idle" | "queued" | "processing" | "completed" | "failed"

interface StoryData {
  title?: string
  chapters?: Array<{
    title: string
    content: string
    image_url?: string
  }>
  [key: string]: unknown
}

interface UseStoryGenerationReturn {
  isGenerating: boolean
  status: StoryStatus
  storyData: StoryData | null
  error: string | null
  generateStory: (topic: string, token: string) => Promise<void>
  reset: () => void
}

const POLLING_INTERVAL = 2000 // 2 seconds

export function useStoryGeneration(): UseStoryGenerationReturn {
  const [isGenerating, setIsGenerating] = useState(false)
  const [status, setStatus] = useState<StoryStatus>("idle")
  const [storyData, setStoryData] = useState<StoryData | null>(null)
  const [error, setError] = useState<string | null>(null)
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null)
  const abortControllerRef = useRef<AbortController | null>(null)

  const fastApiUrl = process.env.NEXT_PUBLIC_FASTAPI_URL

  const pollTaskStatus = useCallback(
    async (taskId: string, token: string) => {
      try {
        const response = await fetch(`${fastApiUrl}/tasks/${taskId}`, {
          method: "GET",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${token}`,
          },
          signal: abortControllerRef.current?.signal,
        })

        // ...

        async (topic: string, token: string) => {
          if (!topic.trim()) {
            setError("Topic cannot be empty")
            return
          }

          // Reset states
          setError(null)
          setStoryData(null)
          setIsGenerating(true)
          setStatus("queued")
          abortControllerRef.current = new AbortController()

          try {
            // Step 1: Send generation request
            const initResponse = await fetch(`${fastApiUrl}/stories/generate-story-async`, {
              method: "POST",
              headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({ topic: topic.trim() }),
              signal: abortControllerRef.current.signal,
            })

            console.log("[v0] Init response status:", initResponse.status)

            if (initResponse.status === 401) {
              throw new Error("Authentication failed. Please log in again.")
            }

            if (initResponse.status === 402) {
              throw new Error("No credits available. Please subscribe to continue generating stories.")
            }

            if (!initResponse.ok) {
              const errorText = await initResponse.text()
              console.error("[v0] API Error on generation request:", errorText)
              throw new Error(`API Error: ${initResponse.status} - ${initResponse.statusText}`)
            }

            const initData = await initResponse.json()
            console.log("[v0] Task ID received:", initData.task_id)

            if (!initData.task_id) {
              throw new Error("No task_id received from API")
            }

            // Step 2: Start polling
            let pollCount = 0
            const maxPolls = 300 // 10 minutes max (300 * 2s)

            pollingIntervalRef.current = setInterval(async () => {
              pollCount++

              if (pollCount > maxPolls) {
                clearInterval(pollingIntervalRef.current!)
                setError("Task took too long to complete")
                setStatus("failed")
                setIsGenerating(false)
                return
              }

              const isDone = await pollTaskStatus(initData.task_id, token)
              if (isDone) {
                clearInterval(pollingIntervalRef.current!)
              }
            }, POLLING_INTERVAL)
          } catch (err) {
            if (err instanceof Error && err.name !== "AbortError") {
              console.error("[v0] Error in generateStory:", err)
              setError(err.message)
              setStatus("failed")
            }
            setIsGenerating(false)
            if (pollingIntervalRef.current) {
              clearInterval(pollingIntervalRef.current)
            }
          }
        },
          [fastApiUrl, pollTaskStatus],
  )

  const reset = useCallback(() => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current)
    }
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
    setIsGenerating(false)
    setStatus("idle")
    setStoryData(null)
    setError(null)
  }, [])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current)
      }
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [])

  return {
    isGenerating,
    status,
    storyData,
    error,
    generateStory,
    reset,
  }
}
