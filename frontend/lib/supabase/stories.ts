import { supabase, createAnonymousClient } from "./client"

export interface Story {
  id: string
  user_id: string
  title: string
  content: string
  prompt?: string
  visibility: "public" | "private"
  created_at: string
  updated_at: string
  profiles?: {
    username: string
  }
}

export interface Chapter {
  title: string
  text: string
}

export interface PaginatedStoriesResult {
  stories: Story[]
  totalCount: number
  totalPages: number
  currentPage: number
  hasNextPage: boolean
  hasPreviousPage: boolean
}

// Client-side story operations only
export const storyOperations = {
  // Save a new story
  async saveStory(
    userId: string, // Recibe userId como argumento
    title: string,
    content: string | Chapter[] | Record<string, any>, // Accept full JSON objects
    prompt?: string,
  ): Promise<{ data: Story | null; error: any }> {
    if (!supabase) {
      return { data: null, error: new Error("Supabase not configured") }
    }
    if (!userId) {
      return { data: null, error: new Error("User ID is required to save story.") }
    }

    try {
      let contentString: string
      if (typeof content === "string") {
        contentString = content
      } else if (Array.isArray(content)) {
        // Legacy: convert chapters array to markdown string
        contentString = content.map((chapter) => `# ${chapter.title}\n\n${chapter.text}`).join("\n\n---\n\n")
      } else if (typeof content === "object" && content !== null) {
        contentString = JSON.stringify(content, null, 2)
      } else {
        contentString = String(content)
      }

      const storyTitle = title || `Story from ${new Date().toLocaleDateString()}`

      const { data, error } = await supabase
        .from("stories")
        .insert({
          user_id: userId,
          title: storyTitle,
          content: contentString,
          prompt: prompt || null,
          visibility: "private",
        })
        .select()
        .single()

      return { data, error }
    } catch (error) {
      console.error("Error saving story:", error)
      return { data: null, error }
    }
  },

  // Get all stories for current user with pagination
  async getUserStories(
    userId: string,
    page = 1,
    limit = 12,
  ): Promise<{ data: PaginatedStoriesResult | null; error: any }> {
    if (!supabase) {
      return { data: null, error: new Error("Supabase not configured") }
    }
    if (!userId) {
      return { data: null, error: new Error("User ID is required to fetch stories.") }
    }

    try {
      const offset = (page - 1) * limit

      // Get total count of user stories
      const { count, error: countError } = await supabase
        .from("stories")
        .select("*", { count: "exact", head: true })
        .eq("user_id", userId)

      if (countError) {
        console.error("Error getting count:", countError)
        throw countError
      }

      // Get paginated user stories
      const { data, error } = await supabase
        .from("stories")
        .select("*")
        .eq("user_id", userId)
        .order("created_at", { ascending: false })
        .range(offset, offset + limit - 1)

      if (error) {
        console.error("Error fetching stories:", error)
        throw error
      }

      const totalCount = count || 0
      const totalPages = Math.ceil(totalCount / limit)

      const result: PaginatedStoriesResult = {
        stories: data || [],
        totalCount,
        totalPages,
        currentPage: page,
        hasNextPage: page < totalPages,
        hasPreviousPage: page > 1,
      }

      return { data: result, error: null }
    } catch (error) {
      console.error("Error fetching stories:", error)
      return { data: null, error }
    }
  },

  // Get public stories with pagination (accessible to all users, including anonymous)
  async getPublicStories(page = 1, limit = 12): Promise<{ data: PaginatedStoriesResult | null; error: any }> {
    // Try to use the main client first, fallback to anonymous client
    let client = supabase

    if (!client) {
      client = createAnonymousClient()
      if (!client) {
        return { data: null, error: new Error("Supabase not configured") }
      }
    }

    try {
      const offset = (page - 1) * limit

      console.log("Fetching public stories with client:", !!client)

      // Get total count of public stories
      const { count, error: countError } = await client
        .from("stories")
        .select("*", { count: "exact", head: true })
        .eq("visibility", "public")

      if (countError) {
        console.error("Error getting count:", countError)
        throw countError
      }

      console.log("Total public stories count:", count)

      // Get paginated public stories
      const { data, error } = await client
        .from("stories")
        .select("*")
        .eq("visibility", "public")
        .order("created_at", { ascending: false })
        .range(offset, offset + limit - 1)

      if (error) {
        console.error("Error getting stories:", error)
        throw error
      }

      let stories = data || []

      // Manual join with profiles to avoid 400 error if FK is missing
      if (stories.length > 0) {
        const userIds = [...new Set(stories.map(s => s.user_id))]

        try {
          const { data: profiles, error: profilesError } = await client
            .from("profiles")
            .select("id, username")
            .in("id", userIds)

          if (!profilesError && profiles) {
            const profileMap = new Map(profiles.map(p => [p.id, p]))

            stories = stories.map(story => ({
              ...story,
              profiles: profileMap.get(story.user_id) || { username: "Anonymous" }
            }))
          }
        } catch (e) {
          console.warn("Error fetching profiles for stories:", e)
        }
      }

      console.log("Fetched stories:", stories.length)

      const totalCount = count || 0
      const totalPages = Math.ceil(totalCount / limit)

      const result: PaginatedStoriesResult = {
        stories: stories,
        totalCount,
        totalPages,
        currentPage: page,
        hasNextPage: page < totalPages,
        hasPreviousPage: page > 1,
      }

      return { data: result, error: null }
    } catch (error) {
      console.error("Error fetching public stories:", error)
      return { data: null, error }
    }
  },

  // Update story visibility
  async updateStoryVisibility(
    storyId: string,
    visibility: "public" | "private",
  ): Promise<{ data: Story | null; error: any }> {
    if (!supabase) {
      return { data: null, error: new Error("Supabase not configured") }
    }
    if (!storyId) {
      return { data: null, error: new Error("Story ID is required to update visibility.") }
    }

    try {
      const { data, error } = await supabase.from("stories").update({ visibility }).eq("id", storyId).select().single()

      return { data, error }
    } catch (error) {
      console.error("Error updating story visibility:", error)
      return { data: null, error }
    }
  },

  // Delete a story and its associated images
  async deleteStory(storyId: string): Promise<{ error: any }> {
    if (!supabase) {
      return { error: new Error("Supabase not configured") }
    }

    try {
      // 1. Fetch story content to find associated images
      const { data: story, error: fetchError } = await supabase
        .from("stories")
        .select("content")
        .eq("id", storyId)
        .single()

      if (fetchError) {
        console.error("Error fetching story for deletion:", fetchError)
        // Proceed to try delete anyway if fetch fails? simpler to just return error
        return { error: fetchError }
      }

      // 2. Extract and delete images if they exist
      if (story?.content) {
        try {
          let content = story.content
          // Parse if string
          if (typeof content === "string") {
            try {
              content = JSON.parse(content)
              if (typeof content === "string") {
                content = JSON.parse(content)
              }
            } catch (e) {
              content = {}
            }
          }

          const bucketName = "cuentee_images"
          const filesToDelete: string[] = []

          // Helper to extract file path from URL
          const getFilePath = (url: string) => {
            if (!url || !url.includes(`/${bucketName}/`)) return null
            const parts = url.split(`/${bucketName}/`)
            return parts.length > 1 ? parts[1] : null
          }

          // A. Cover Image
          if (content?.cover_image_url) {
            const path = getFilePath(content.cover_image_url)
            if (path) filesToDelete.push(path)
          }

          // B. Chapter Images
          if (Array.isArray(content?.chapters)) {
            content.chapters.forEach((chapter: any) => {
              if (chapter?.image_url) {
                const path = getFilePath(chapter.image_url)
                if (path) filesToDelete.push(path)
              }
            })
          }

          // C. Batch Delete
          if (filesToDelete.length > 0) {
            console.log("Deleting images from storage:", filesToDelete)

            const { error: storageError } = await supabase
              .storage
              .from(bucketName)
              .remove(filesToDelete)

            if (storageError) {
              console.error("Error deleting images from storage:", storageError)
            } else {
              console.log(`Successfully deleted ${filesToDelete.length} images`)
            }
          }

        } catch (parseError) {
          console.error("Error parsing story content for image deletion:", parseError)
        }
      }

      // 3. Delete the story record
      const { error } = await supabase.from("stories").delete().eq("id", storyId)

      return { error }
    } catch (error) {
      console.error("Error deleting story:", error)
      return { error }
    }
  },
}
