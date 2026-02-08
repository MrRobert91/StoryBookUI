"use client"

import { useState } from "react"
import { ChevronDown, ChevronUp, Info, User, Clock, BookOpen, Microscope, Target, Sparkles, Languages } from "lucide-react"

interface StoryMetadataProps {
    storyType?: "open" | "guided"
    metadata?: Record<string, any>
    prompt?: string
    className?: string
}

export default function StoryMetadata({ storyType = "open", metadata = {}, prompt, className = "" }: StoryMetadataProps) {
    const [isExpanded, setIsExpanded] = useState(false)

    if (!metadata && !prompt) return null

    const isGuided = storyType === "guided"

    const renderMetadataItem = (icon: React.ReactNode, label: string, value: any) => {
        if (value === undefined || value === null || value === "") return null
        return (
            <div className="flex items-center gap-2 text-sm text-gray-700 bg-white/50 px-3 py-1.5 rounded-full border border-purple-100 shadow-sm">
                <span className="text-purple-500">{icon}</span>
                <span className="font-medium text-gray-500">{label}:</span>
                <span className="text-gray-900">{value.toString()}</span>
            </div>
        )
    }

    return (
        <div className={`mt-2 ${className}`}>
            <button
                onClick={(e) => {
                    e.stopPropagation()
                    setIsExpanded(!isExpanded)
                }}
                className="flex items-center gap-1.5 text-sm font-semibold text-purple-700 hover:text-purple-800 transition-colors bg-purple-50 px-3 py-1 rounded-md mb-2"
            >
                <Info className="h-4 w-4" />
                {isGuided ? "Story Parameters" : "Story Details"}
                {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
            </button>

            {isExpanded && (
                <div className="flex flex-wrap gap-2 animate-in fade-in slide-in-from-top-1 duration-200">
                    {isGuided ? (
                        <>
                            {renderMetadataItem(<Clock className="h-4 w-4" />, "Age Group", metadata.age_group)}
                            {renderMetadataItem(<BookOpen className="h-4 w-4" />, "Length", `${metadata.story_length} chapters`)}
                            {renderMetadataItem(<User className="h-4 w-4" />, "Protagonist", metadata.protagonist_name)}
                            {renderMetadataItem(<Sparkles className="h-4 w-4" />, "Description", metadata.protagonist_description)}
                            {renderMetadataItem(<Microscope className="h-4 w-4" />, "Scientific", metadata.scientific ? "Yes" : "No")}
                            {renderMetadataItem(<Target className="h-4 w-4" />, "Topic", metadata.topic)}
                            {renderMetadataItem(<Target className="h-4 w-4" />, "Mission", metadata.mission)}
                            {renderMetadataItem(<Sparkles className="h-4 w-4" />, "Visual Style", metadata.visual_style)}
                        </>
                    ) : (
                        <>
                            {renderMetadataItem(<Languages className="h-4 w-4" />, "Language", metadata.language)}
                            {renderMetadataItem(<BookOpen className="h-4 w-4" />, "Length", `${metadata.story_length || '3'} chapters`)}
                            {renderMetadataItem(<Sparkles className="h-4 w-4" />, "Style", metadata.artistic_style)}
                            {prompt && (
                                <div className="w-full mt-1 p-3 bg-purple-50/50 rounded-lg border border-purple-100 text-sm italic text-purple-700">
                                    <span className="font-bold not-italic block mb-1">Prompt:</span>
                                    "{prompt}"
                                </div>
                            )}
                        </>
                    )}
                </div>
            )}
        </div>
    )
}
