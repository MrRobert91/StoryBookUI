"use client"

import type React from "react"

import { useState } from "react"
import { X, Trash2, ChevronDown, ChevronUp, Download } from "lucide-react"
import type { Story } from "@/lib/supabase/stories"
import MarkdownRenderer from "./markdown-renderer"
import { getPdfUrl } from "./story-preview"
import StoryMetadata from "./story-metadata"

interface StoryModalProps {
  story: Story
  onClose: () => void
  onDelete?: (id: string) => Promise<void>
}

export default function StoryModal({ story, onClose, onDelete }: StoryModalProps) {
  const [isPromptExpanded, setIsPromptExpanded] = useState(false)

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  // Handle backdrop click
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      onClick={handleBackdropClick}
    >
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b shrink-0">
          <div className="flex-1 mr-4">
            <h2 className="text-2xl font-bold text-gray-900">{story.title}</h2>
            <p className="text-gray-600 text-sm mt-1">
              Created by <span className="font-medium text-purple-700">{story.profiles?.username || "Anonymous"}</span> on {formatDate(story.created_at)}
            </p>
            <StoryMetadata
              storyType={story.story_type}
              metadata={story.metadata}
              prompt={story.story_type === "guided" ? undefined : story.prompt}
              className="mt-3"
            />
          </div>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full transition-colors self-start">
            <X className="h-6 w-6 text-gray-500" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto flex-1">
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border-l-4 border-purple-500">
            <MarkdownRenderer content={story.content} />
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end gap-3 p-6 border-t bg-gray-50">
          {onDelete && (
            <button
              onClick={() => {
                if (window.confirm("Are you sure you want to delete this story? This action cannot be undone.")) {
                  onDelete(story.id)
                }
              }}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors flex items-center gap-2"
            >
              <Trash2 className="h-4 w-4" />
              Delete Story
            </button>
          )}
          {getPdfUrl(story.content) ? (
            <a
              href={getPdfUrl(story.content)!}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors flex items-center gap-2"
            >
              <Download className="h-4 w-4" />
              Download PDF
            </a>
          ) : (
            <button
              onClick={() => {
                navigator.clipboard.writeText(typeof story.content === 'string' ? story.content : JSON.stringify(story.content))
                alert("Story copied to clipboard! (PDF not available for this story)")
              }}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
            >
              Copy Story
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
