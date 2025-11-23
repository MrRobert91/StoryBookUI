"use client"

interface MarkdownRendererProps {
  content: string
}

export default function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const renderContent = () => {
    try {
      let jsonData: any = null
      let chapters: any[] = []

      // Try to parse as JSON
      try {
        jsonData = JSON.parse(content)
        if (jsonData.chapters && Array.isArray(jsonData.chapters)) {
          chapters = jsonData.chapters
        }
      } catch {
        // Not JSON, continue with markdown parsing
      }

      // If we have chapters with the new structure (title, content, image_url)
      if (chapters.length > 0 && chapters[0].content !== undefined) {
        return (
          <div className="space-y-6">
            {chapters.map((chapter: any, index: number) => (
              <div key={index}>
                <h3 className="text-lg font-bold text-gray-900 mb-3">{chapter.title}</h3>
                <p className="text-gray-800 leading-relaxed whitespace-pre-line mb-4">{chapter.content}</p>
                {chapter.image_url && (
                  <div className="my-4">
                    <img
                      src={chapter.image_url || "/placeholder.svg"}
                      alt={chapter.title}
                      className="w-full max-w-2xl h-auto rounded-lg shadow-md object-cover aspect-square"
                      onError={(e) => {
                        console.error("[v0] Failed to load chapter image:", chapter.image_url)
                        e.currentTarget.style.display = "none"
                      }}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        )
      }

      // Original markdown parsing logic for backward compatibility
      let parsedContent = content

      try {
        if (jsonData.chapters && Array.isArray(jsonData.chapters)) {
          parsedContent = jsonData.chapters
            .map((chapter: any) => {
              if (typeof chapter === "object" && chapter !== null) {
                if ("title" in chapter && "text" in chapter) {
                  return `## ${chapter.title}\n\n${chapter.text}`
                }
                if ("content" in chapter) {
                  return chapter.content
                }
              }
              return String(chapter)
            })
            .join("\n\n")
        }
      } catch {
        parsedContent = content
      }

      // Split by markdown headings (##) and process
      const parts = parsedContent.split(/(?=##\s)/)

      return (
        <div className="space-y-4">
          {parts.map((part, index) => {
            const trimmedPart = part.trim()
            if (!trimmedPart) return null

            // Check if this part starts with ##
            if (trimmedPart.startsWith("##")) {
              const lines = trimmedPart.split("\n")
              const titleLine = lines[0].replace(/^##\s+/, "")
              const bodyLines = lines.slice(1).join("\n").trim()

              return (
                <div key={index}>
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{titleLine}</h3>
                  {renderBodyWithImages(bodyLines)}
                </div>
              )
            }

            return (
              trimmedPart && (
                <p key={index} className="text-gray-800 leading-relaxed whitespace-pre-line">
                  {trimmedPart}
                </p>
              )
            )
          })}
        </div>
      )
    } catch (error) {
      console.error("[v0] Error rendering markdown:", error)
      return <p className="text-gray-800 leading-relaxed whitespace-pre-line">{content}</p>
    }
  }

  const renderBodyWithImages = (text: string) => {
    // Match image URLs or image placeholders
    // Supports: [URL], ![alt](url), or image_url: value patterns
    const urlRegex =
      /(?:\[(?:IMAGE[^\]]*|https?:\/\/[^\]]*)\]|!\[([^\]]*)\]$$([^)]+)$$|(https?:\/\/[^\s]+\.(?:jpg|jpeg|png|gif|webp|svg)))/gi

    const parts = text.split(urlRegex)
    const elements = []

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i]

      if (!part) continue

      // Check if this is a URL (direct image URL)
      if (
        part.startsWith("http://") ||
        part.startsWith("https://") ||
        (part.startsWith("[") && part.includes("http"))
      ) {
        const imageUrl = part.startsWith("[") ? part.slice(1, -1) : part
        if (imageUrl.match(/\.(jpg|jpeg|png|gif|webp|svg)$/i)) {
          elements.push(
            <div key={`img-${i}`} className="my-4">
              <img
                src={imageUrl || "/placeholder.svg"}
                alt="Story illustration"
                className="w-full max-w-2xl h-auto rounded-lg shadow-md object-cover aspect-square"
                onError={(e) => {
                  console.error("Failed to load image:", imageUrl)
                  e.currentTarget.style.display = "none"
                }}
              />
            </div>,
          )
          continue
        }
      }

      // If it's text content
      if (part && part.trim() && !part.startsWith("[") && !part.startsWith("!")) {
        elements.push(
          <p key={`text-${i}`} className="text-gray-800 leading-relaxed whitespace-pre-line">
            {part}
          </p>,
        )
      }
    }

    return elements.length > 0 ? elements : <p className="text-gray-800 leading-relaxed">{text}</p>
  }

  return <>{renderContent()}</>
}
