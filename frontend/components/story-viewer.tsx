"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BookOpen } from "lucide-react"

interface Chapter {
  title: string
  content: string
  image_url?: string
}

interface StoryViewerProps {
  chapters: Chapter[]
  title?: string
}

export default function StoryViewer({ chapters, title }: StoryViewerProps) {
  // Check if chapters have the new structure with image_url
  const hasImages = chapters.length > 0 && "image_url" in chapters[0]

  if (hasImages) {
    // Render with images
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-green-600" />
            {title || "Your AI-Generated Story"}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border-l-4 border-purple-500 space-y-6">
            {chapters.map((chapter: any, index: number) => (
              <div key={index}>
                <h3 className="text-lg font-bold text-gray-900 mb-3">{chapter.title}</h3>
                <p className="text-gray-800 leading-relaxed">{chapter.content}</p>
                {chapter.image_url && (
                  <div className="my-4">
                    <img
                      src={chapter.image_url || "/placeholder.svg"}
                      alt={chapter.title}
                      className="w-full max-w-2xl h-auto rounded-lg shadow-md object-cover aspect-square"
                      onError={(e) => {
                        console.error("[v0] Failed to load image:", chapter.image_url)
                        e.currentTarget.style.display = "none"
                      }}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="flex gap-4 pt-4 border-t">
            <button
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
              onClick={() => console.log("Save story")}
            >
              Save Story
            </button>
            <button
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
              onClick={() => console.log("Share story")}
            >
              Share
            </button>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Create Another
            </button>
          </div>
        </CardContent>
      </Card>
    )
  }

  // Original rendering logic for markdown-based chapters
  const fullStoryContent = chapters.map((chapter) => `# ${chapter.title}\n\n${chapter.content}`).join("\n\n---\n\n")

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BookOpen className="h-5 w-5 text-green-600" />
          {title || "Your AI-Generated Story"}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border-l-4 border-purple-500">
          <div className="whitespace-pre-line text-gray-800 leading-relaxed">{fullStoryContent}</div>
        </div>

        <div className="flex gap-4 pt-4 border-t">
          <button
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
            onClick={() => console.log("Save story")}
          >
            Save Story
          </button>
          <button
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
            onClick={() => console.log("Share story")}
          >
            Share
          </button>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Create Another
          </button>
        </div>
      </CardContent>
    </Card>
  )
}
