"use client"

import { useEffect, useState } from "react"
import Navbar from "@/components/navbar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { storyOperations, type Story, type PaginatedStoriesResult } from "@/lib/supabase/stories"
import { BookOpen, Calendar, User, Loader2, AlertCircle, ChevronLeft, ChevronRight, Eye } from "lucide-react"
import StoryModal from "@/components/story-modal"
import { getStoryPreview } from "@/components/story-preview"

const ITEMS_PER_PAGE_OPTIONS = [12, 24, 48, 96]

export default function GalleryPage() {
  const [storiesData, setStoriesData] = useState<PaginatedStoriesResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(12)
  const [selectedStory, setSelectedStory] = useState<Story | null>(null)

  useEffect(() => {
    loadPublicStories(currentPage, itemsPerPage)
  }, [currentPage, itemsPerPage])

  const loadPublicStories = async (page: number, limit: number) => {
    setLoading(true)
    setError(null)

    try {
      const { data, error } = await storyOperations.getPublicStories(page, limit)

      if (error) {
        throw error
      }

      setStoriesData(data)
    } catch (err) {
      console.error("Error loading public stories:", err)
      setError(err instanceof Error ? err.message : "Failed to load stories")
    } finally {
      setLoading(false)
    }
  }

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage)
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  const handleItemsPerPageChange = (newLimit: number) => {
    setItemsPerPage(newLimit)
    setCurrentPage(1) // Reset to first page when changing items per page
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }

  const truncateContent = (content: string, maxLength = 200) => {
    if (content.length <= maxLength) return content
    return content.substring(0, maxLength) + "..."
  }

  const getPageNumbers = () => {
    if (!storiesData) return []

    const { currentPage, totalPages } = storiesData
    const pages = []
    const maxVisiblePages = 5

    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2))
    const endPage = Math.min(totalPages, startPage + maxVisiblePages - 1)

    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1)
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i)
    }

    return pages
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Story <span className="text-purple-600">Gallery</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Discover magical tales created by our community. Explore stories from around the world and get inspired for
            your own creations.
          </p>
        </div>

        {/* Controls */}
        <div className="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-700">Stories per page:</span>
            <select
              value={itemsPerPage}
              onChange={(e) => handleItemsPerPageChange(Number(e.target.value))}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              {ITEMS_PER_PAGE_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>

          {storiesData && (
            <div className="text-sm text-gray-600">
              Showing {storiesData.stories.length} of {storiesData.totalCount} stories
            </div>
          )}
        </div>

        {/* Content */}
        {loading ? (
          <div className="flex items-center justify-center py-24">
            <div className="text-center">
              <Loader2 className="h-12 w-12 animate-spin text-purple-600 mx-auto mb-4" />
              <p className="text-gray-600 text-lg">Loading magical stories...</p>
            </div>
          </div>
        ) : error ? (
          <div className="flex items-center justify-center py-24">
            <div className="text-center">
              <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Stories</h3>
              <p className="text-gray-600 mb-6">{error}</p>
              <button
                onClick={() => loadPublicStories(currentPage, itemsPerPage)}
                className="px-6 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors"
              >
                Try Again
              </button>
            </div>
          </div>
        ) : !storiesData || storiesData.stories.length === 0 ? (
          <div className="text-center py-24">
            <BookOpen className="h-20 w-20 text-gray-300 mx-auto mb-6" />
            <h3 className="text-2xl font-semibold text-gray-900 mb-4">No Public Stories Yet</h3>
            <p className="text-gray-600 mb-8 max-w-md mx-auto">
              Be the first to share your magical tale with the community! Create a story and make it public to appear in
              the gallery.
            </p>
            <a
              href="/make-tale"
              className="inline-flex items-center px-6 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors"
            >
              <BookOpen className="h-4 w-4 mr-2" />
              Create Your First Story
            </a>
          </div>
        ) : (
          <>
            {/* Stories Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-12">
              {storiesData.stories.map((story) => (
                <Card key={story.id} className="hover:shadow-lg transition-shadow cursor-pointer group">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-lg font-semibold text-gray-900 line-clamp-2 group-hover:text-purple-600 transition-colors">
                      {story.title}
                    </CardTitle>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      <div className="flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        {formatDate(story.created_at)}
                      </div>
                      <div className="flex items-center gap-1">
                        <User className="h-3 w-3" />
                        Anonymous
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="pt-0">
                    {story.prompt && (
                      <p className="text-purple-600 text-xs mb-3 italic">"{truncateContent(story.prompt, 80)}"</p>
                    )}
                    <p className="text-gray-700 text-sm leading-relaxed mb-4 line-clamp-4">
                      {truncateContent(getStoryPreview(story.content))}
                    </p>
                    <button
                      onClick={() => setSelectedStory(story)}
                      className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors text-sm"
                    >
                      <Eye className="h-4 w-4" />
                      Read Full Story
                    </button>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Pagination */}
            {storiesData.totalPages > 1 && (
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="text-sm text-gray-600">
                  Page {storiesData.currentPage} of {storiesData.totalPages}
                </div>

                <div className="flex items-center gap-2">
                  {/* Previous Button */}
                  <button
                    onClick={() => handlePageChange(storiesData.currentPage - 1)}
                    disabled={!storiesData.hasPreviousPage}
                    className={`flex items-center gap-1 px-3 py-2 rounded-md text-sm transition-colors ${
                      storiesData.hasPreviousPage
                        ? "bg-white border border-gray-300 text-gray-700 hover:bg-gray-50"
                        : "bg-gray-100 text-gray-400 cursor-not-allowed"
                    }`}
                  >
                    <ChevronLeft className="h-4 w-4" />
                    Previous
                  </button>

                  {/* Page Numbers */}
                  <div className="hidden sm:flex items-center gap-1">
                    {getPageNumbers().map((pageNum) => (
                      <button
                        key={pageNum}
                        onClick={() => handlePageChange(pageNum)}
                        className={`px-3 py-2 rounded-md text-sm transition-colors ${
                          pageNum === storiesData.currentPage
                            ? "bg-purple-600 text-white"
                            : "bg-white border border-gray-300 text-gray-700 hover:bg-gray-50"
                        }`}
                      >
                        {pageNum}
                      </button>
                    ))}
                  </div>

                  {/* Next Button */}
                  <button
                    onClick={() => handlePageChange(storiesData.currentPage + 1)}
                    disabled={!storiesData.hasNextPage}
                    className={`flex items-center gap-1 px-3 py-2 rounded-md text-sm transition-colors ${
                      storiesData.hasNextPage
                        ? "bg-white border border-gray-300 text-gray-700 hover:bg-gray-50"
                        : "bg-gray-100 text-gray-400 cursor-not-allowed"
                    }`}
                  >
                    Next
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </div>

                <div className="text-sm text-gray-600">{storiesData.totalCount} total stories</div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Story Modal */}
      {selectedStory && <StoryModal story={selectedStory} onClose={() => setSelectedStory(null)} />}
    </div>
  )
}
