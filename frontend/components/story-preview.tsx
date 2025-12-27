"use client"

export function getStoryPreview(content: string | any): string {
  if (!content) return ""

  try {
    let parsed = content

    // If string, parse it
    if (typeof content === "string") {
      try {
        parsed = JSON.parse(content)
        // Handle double stringification
        if (typeof parsed === "string") {
          parsed = JSON.parse(parsed)
        }
      } catch {
        // If parsing fails, return as is (legacy plain text content)
        return content
      }
    }

    // If simple object with tale/description (legacy)
    if (parsed.tale) return parsed.tale

    // If it has chapters array
    if (Array.isArray(parsed.chapters) && parsed.chapters.length > 0) {
      const chaptersText = parsed.chapters
        .map((chapter: any) => {
          if (typeof chapter === "string") {
            return chapter
          } else if (chapter.text) {
            return chapter.text
          } else if (chapter.content) {
            return chapter.content
          }
          return ""
        })
        .join("\n\n")

      return chaptersText
    }
  } catch (e) {
    console.warn("Error parsing story preview:", e)
  }

  return typeof content === "string" ? content : "Preview not available"
}

export function getCoverImage(content: string | any): string | null {
  if (!content) return null

  try {
    // If it's already an object (Supabase JSONB handling)
    if (typeof content === 'object') {
      return content.cover_image_url || null
    }

    // If it's a string, verify it's not a double-encoded string or just parse it
    const parsed = JSON.parse(content)

    // Sometimes double parsing is needed if it was stringified twice
    if (typeof parsed === 'string') {
      try {
        const doubleParsed = JSON.parse(parsed)
        if (typeof doubleParsed === 'object') {
          return doubleParsed.cover_image_url || null
        }
      } catch {
        return null
      }
    }

    return parsed.cover_image_url || null
  } catch (e) {
    console.error("Error parsing cover image from content:", e)
    return null
  }
}
