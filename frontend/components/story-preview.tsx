"use client"

export function getStoryPreview(content: string): string {
  try {
    // Try to parse as JSON
    const parsed = JSON.parse(content)

    // If it has a chapters array, extract text from chapters
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
    // Not JSON, return as is
  }

  return content
}

export function getCoverImage(content: string): string | null {
  try {
    const parsed = JSON.parse(content)
    return parsed.cover_image_url || null
  } catch (e) {
    return null
  }
}
