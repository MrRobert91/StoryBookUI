"use client"

import { useState, useEffect } from "react"
import type { User } from "@supabase/supabase-js"
import { supabase } from "@/lib/supabase/client"
import { profileOperations, type UserProfile } from "@/lib/supabase/profile-operations"
import { storyOperations, type Story } from "@/lib/supabase/stories"
import StoryModal from "./story-modal"
import StripeModal from "./stripe-modal"
import { Loader2, Edit2, Check, X, Globe, Lock } from "lucide-react"
import { getStoryPreview } from "./story-preview"

interface AccountContentProps {
  user: User
}

export default function AccountContent({ user }: AccountContentProps) {
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [stories, setStories] = useState<Story[]>([])
  const [loading, setLoading] = useState(true)
  const [storiesLoading, setStoriesLoading] = useState(true)
  const [selectedStory, setSelectedStory] = useState<Story | null>(null)
  const [showStripeModal, setShowStripeModal] = useState(false)
  const [editingUsername, setEditingUsername] = useState(false)
  const [newUsername, setNewUsername] = useState("")
  const [usernameStatus, setUsernameStatus] = useState<{
    checking: boolean
    available: boolean | null
    error: string | null
  }>({
    checking: false,
    available: null,
    error: null,
  })

  // Username validation regex
  const usernameRegex = /^[a-z0-9_.]{3,20}$/
  const invalidPatternRegex = /^[._]|[._]$|[._]{2,}/

  useEffect(() => {
    if (user) {
      loadProfile()
      loadStories()
    }
  }, [user])

  // Username availability check
  useEffect(() => {
    if (!editingUsername || !newUsername || newUsername.length < 3 || newUsername === profile?.username) {
      setUsernameStatus({ checking: false, available: null, error: null })
      return
    }

    // Validate format first
    if (!usernameRegex.test(newUsername)) {
      setUsernameStatus({
        checking: false,
        available: false,
        error: "Username must be 3-20 characters, lowercase letters, numbers, dots and underscores only",
      })
      return
    }

    if (invalidPatternRegex.test(newUsername)) {
      setUsernameStatus({
        checking: false,
        available: false,
        error: "Username cannot start/end with . or _ or have consecutive . or _",
      })
      return
    }

    const timeoutId = setTimeout(async () => {
      setUsernameStatus({ checking: true, available: null, error: null })

      try {
        const { available, error } = await profileOperations.checkUsernameAvailability(newUsername)

        if (error) {
          setUsernameStatus({
            checking: false,
            available: false,
            error: "Error checking username availability",
          })
        } else {
          setUsernameStatus({
            checking: false,
            available,
            error: available ? null : "Username is already taken",
          })
        }
      } catch (error) {
        setUsernameStatus({
          checking: false,
          available: false,
          error: "Error checking username availability",
        })
      }
    }, 500) // 500ms debounce

    return () => clearTimeout(timeoutId)
  }, [newUsername, editingUsername, profile?.username])

  const loadProfile = async () => {
    try {
      const { data, error } = await profileOperations.getUserProfile(user)
      if (error) {
        console.error("Error loading profile:", error)
      } else {
        setProfile(data)
      }
    } catch (error) {
      console.error("Error loading profile:", error)
    } finally {
      setLoading(false)
    }
  }

  const loadStories = async () => {
    try {
      console.log("Loading stories for user ID:", user.id)
      const { data, error } = await storyOperations.getUserStories(user.id) // Pass user.id instead of user object
      if (error) {
        console.error("Error loading stories:", error)
      } else {
        console.log("Stories loaded successfully:", data?.length || 0)
        setStories(data || [])
      }
    } catch (error) {
      console.error("Error loading stories:", error)
    } finally {
      setStoriesLoading(false)
    }
  }

  const handleUsernameEdit = () => {
    setEditingUsername(true)
    setNewUsername(profile?.username || "")
  }

  const handleUsernameSave = async () => {
    if (!profile || !newUsername || usernameStatus.available !== true) {
      return
    }

    try {
      const { data, error } = await profileOperations.updateUsername(profile.id, newUsername)
      if (error) {
        console.error("Error updating username:", error)
        alert("Error updating username. Please try again.")
      } else {
        setProfile(data)
        setEditingUsername(false)
        setUsernameStatus({ checking: false, available: null, error: null })
      }
    } catch (error) {
      console.error("Error updating username:", error)
      alert("Error updating username. Please try again.")
    }
  }

  const handleUsernameCancel = () => {
    setEditingUsername(false)
    setNewUsername(profile?.username || "")
    setUsernameStatus({ checking: false, available: null, error: null })
  }

  const handleSignOut = async () => {
    try {
      await supabase?.auth.signOut()
    } catch (error) {
      console.error("Error signing out:", error)
    }
  }

  const toggleStoryVisibility = async (story: Story) => {
    const newVisibility = story.visibility === "public" ? "private" : "public"

    try {
      const { error } = await storyOperations.updateStoryVisibility(story.id, newVisibility)

      if (error) {
        console.error("Error updating story visibility:", error)
        alert("Error updating story visibility. Please try again.")
      } else {
        // Update the story in the local state
        setStories((prevStories) =>
          prevStories.map((s) => (s.id === story.id ? { ...s, visibility: newVisibility } : s)),
        )
      }
    } catch (error) {
      console.error("Error updating story visibility:", error)
      alert("Error updating story visibility. Please try again.")
    }
  }

  const handleDeleteStory = async (storyId: string) => {
    try {
      const { error } = await storyOperations.deleteStory(storyId)

      if (error) {
        console.error("Error deleting story:", error)
        alert("Error deleting story. Please try again.")
        return false
      } else {
        // Remove the story from the local state
        setStories((prevStories) => prevStories.filter((s) => s.id !== storyId))
        return true
      }
    } catch (error) {
      console.error("Error deleting story:", error)
      alert("Error deleting story. Please try again.")
      return false
    }
  }

  const truncateContent = (content: string) => {
    return content.substring(0, 100) + "..."
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-purple-600" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Profile Section */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-gray-900">My Account</h1>
            <button
              onClick={handleSignOut}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
            >
              Sign Out
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Profile Information</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <p className="mt-1 text-sm text-gray-900">{user.email}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Username</label>
                  {editingUsername ? (
                    <div className="mt-1 space-y-2">
                      <div className="relative">
                        <input
                          type="text"
                          value={newUsername}
                          onChange={(e) => setNewUsername(e.target.value.toLowerCase())}
                          className={`w-full px-3 py-2 pr-10 bg-white border rounded-md text-gray-900 focus:outline-none focus:ring-2 focus:border-transparent ${usernameStatus.error
                            ? "border-red-300 focus:ring-red-500"
                            : usernameStatus.available === true
                              ? "border-green-300 focus:ring-green-500"
                              : "border-gray-300 focus:ring-purple-500"
                            }`}
                        />
                        <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                          {usernameStatus.checking ? (
                            <Loader2 className="h-4 w-4 animate-spin text-gray-400" />
                          ) : usernameStatus.available === true ? (
                            <Check className="h-4 w-4 text-green-500" />
                          ) : usernameStatus.available === false ? (
                            <X className="h-4 w-4 text-red-500" />
                          ) : null}
                        </div>
                      </div>
                      {usernameStatus.error && <p className="text-xs text-red-600">{usernameStatus.error}</p>}
                      {usernameStatus.available === true && (
                        <p className="text-xs text-green-600">Username is available!</p>
                      )}
                      <div className="flex space-x-2">
                        <button
                          onClick={handleUsernameSave}
                          disabled={usernameStatus.available !== true}
                          className="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400"
                        >
                          Save
                        </button>
                        <button
                          onClick={handleUsernameCancel}
                          className="px-3 py-1 text-sm bg-gray-600 text-white rounded hover:bg-gray-700"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="mt-1 flex items-center space-x-2">
                      <p className="text-sm text-gray-900">{profile?.username || "Not set"}</p>
                      <button
                        onClick={handleUsernameEdit}
                        className="text-purple-600 hover:text-purple-700"
                        title="Edit username"
                      >
                        <Edit2 className="h-4 w-4" />
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>

            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Subscription</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Current Plan</label>
                  <p className="mt-1 text-sm text-gray-900 capitalize">{profile?.plan || "Free"}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Credits Remaining</label>
                  <p className="mt-1 text-sm text-gray-900">{profile?.credits || 0}</p>
                </div>
                {profile?.plan === "free" && (
                  <button
                    onClick={() => setShowStripeModal(true)}
                    className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors"
                  >
                    Upgrade to Plus
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Stories Section */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-6">My Stories</h2>

          {storiesLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-6 w-6 animate-spin text-purple-600" />
            </div>
          ) : stories.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500">No stories yet. Create your first story!</p>
              <button
                onClick={() => (window.location.href = "/make-tale")}
                className="mt-4 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors"
              >
                Create Your First Story
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {stories.map((story) => (
                <div key={story.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-medium text-gray-900 truncate flex-1">
                      {story.title || story.prompt || "Untitled Story"}
                    </h3>
                    <div className="flex items-center space-x-2 ml-2">
                      {/* Visibility indicator */}
                      <div className="flex items-center">
                        {story.visibility === "public" ? (
                          <Globe className="h-4 w-4 text-green-600" title="Public" />
                        ) : (
                          <Lock className="h-4 w-4 text-gray-600" title="Private" />
                        )}
                      </div>
                      {/* Visibility toggle button */}
                      <button
                        onClick={() => toggleStoryVisibility(story)}
                        className={`px-2 py-1 text-xs rounded transition-colors ${story.visibility === "public"
                          ? "bg-green-100 text-green-800 hover:bg-green-200"
                          : "bg-gray-100 text-gray-800 hover:bg-gray-200"
                          }`}
                        title={story.visibility === "public" ? "Make Private" : "Make Public"}
                      >
                        {story.visibility === "public" ? "Public" : "Private"}
                      </button>
                    </div>
                  </div>
                  {story.prompt && <p className="text-xs text-purple-600 mb-2 italic">"{story.prompt}"</p>}
                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                    {typeof story.content === "string"
                      ? truncateContent(getStoryPreview(story.content))
                      : "Generated story"}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">{new Date(story.created_at).toLocaleDateString()}</span>
                    <button
                      onClick={() => setSelectedStory(story)}
                      className="text-purple-600 hover:text-purple-700 text-sm font-medium"
                    >
                      Read Story
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modals */}
      {selectedStory && (
        <StoryModal
          story={selectedStory}
          onClose={() => setSelectedStory(null)}
          onDelete={async (id) => {
            const success = await handleDeleteStory(id)
            if (success) {
              setSelectedStory(null)
            }
          }}
        />
      )}
      {showStripeModal && <StripeModal isOpen={showStripeModal} onClose={() => setShowStripeModal(false)} />}
    </div>
  )
}
