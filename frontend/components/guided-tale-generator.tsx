"use client"

import { useState, useEffect } from "react"
import { useAuth } from "@/components/auth-provider"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Loader2, Sparkles, AlertCircle, Compass } from "lucide-react"
import StoryViewer from "./story-viewer"
import { supabase } from "@/lib/supabase/client"
import { useStoryGeneration } from "@/hooks/use-story-generation"

interface Chapter {
    title: string
    content: string
    image_url?: string
}

const SCIENTIFIC_TOPICS = {
    "3-5": [
        { value: "shapes_sizes", label: "Tamaños y formas" },
        { value: "human_body", label: "Cuerpo humano" },
    ],
    "5-8": [
        { value: "sound", label: "Sonido" },
        { value: "water_changes", label: "Agua y cambios" },
    ],
}

const MISSIONS = {
    "shapes_sizes": [
        { value: "land_of_shapes", label: "El país de las formas" },
        { value: "big_or_small", label: "Grande o pequeño" },
    ],
    "human_body": [
        { value: "five_senses", label: "Los cinco super sentidos" },
        { value: "brave_tooth", label: "El diente valiente" },
    ],
    "sound": [
        { value: "lost_orchestra", label: "La orquesta perdida" },
        { value: "mysterious_echo", label: "El eco misterioso" },
    ],
    "water_changes": [
        { value: "traveling_drop", label: "La gota viajera" },
        { value: "melting_ice", label: "El hielo que se derrite" },
    ],
}

export default function GuidedTaleGenerator() {
    const { user } = useAuth()
    const {
        isGenerating,
        status,
        storyData,
        error: generationError,
        generateStory
    } = useStoryGeneration()

    const [formData, setFormData] = useState({
        age: "",
        protagonistName: "",
        protagonistDesc: "",
        scientificTopic: "",
        mission: "",
        visualStyle: "",
    })

    const [mounted, setMounted] = useState(false)

    useEffect(() => {
        setMounted(true)
    }, [])

    const handleInputChange = (field: string, value: string) => {
        setFormData((prev) => ({
            ...prev,
            [field]: value,
            // Reset dependent fields
            ...(field === "age" ? { scientificTopic: "", mission: "" } : {}),
            ...(field === "scientificTopic" ? { mission: "" } : {}),
        }))
    }

    const isFormValid = () => {
        return (
            formData.age &&
            formData.protagonistName &&
            formData.protagonistDesc &&
            formData.scientificTopic &&
            formData.mission &&
            formData.visualStyle
        )
    }

    const handleGenerate = async () => {
        if (!isFormValid()) return

        try {
            const { data: { session } } = await supabase.auth.getSession()
            if (!session?.access_token) throw new Error("Authentication required")

            await generateStory(
                {
                    age_group: formData.age,
                    protagonist: `${formData.protagonistName}, ${formData.protagonistDesc}`,
                    scientific_topic: formData.scientificTopic,
                    mission: formData.mission,
                    visual_style: formData.visualStyle,
                },
                session.access_token,
                "/stories/generate_guided_story_async"
            )
        } catch (err) {
            console.error("Error initiating generation:", err)
        }
    }

    if (!mounted) return null

    return (
        <div className="space-y-8">
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Compass className="h-5 w-5 text-teal-600" />
                        Guided Story Configuration
                    </CardTitle>
                    <CardDescription>Customize your educational adventure!</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Age Selection */}
                    <div className="space-y-2">
                        <Label>Age Group</Label>
                        <RadioGroup
                            className="flex gap-4"
                            value={formData.age}
                            onValueChange={(val) => handleInputChange("age", val)}
                        >
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="3-5" id="age-3-5" />
                                <Label htmlFor="age-3-5">3-5 Years</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="5-8" id="age-5-8" />
                                <Label htmlFor="age-5-8">6-8 Years</Label>
                            </div>
                        </RadioGroup>
                    </div>

                    {/* Protagonist */}
                    <div className="grid md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="protagonistName">Protagonist Name</Label>
                            <Input
                                id="protagonistName"
                                placeholder="e.g. Luna"
                                value={formData.protagonistName}
                                onChange={(e) => handleInputChange("protagonistName", e.target.value)}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="protagonistDesc">Protagonist Description</Label>
                            <Input
                                id="protagonistDesc"
                                placeholder="e.g. A brave little cat"
                                value={formData.protagonistDesc}
                                onChange={(e) => handleInputChange("protagonistDesc", e.target.value)}
                            />
                        </div>
                    </div>

                    {/* Scientific Topic - Native Select */}
                    <div className="space-y-2">
                        <Label htmlFor="scientificTopic">Scientific Topic</Label>
                        <div className="relative">
                            <select
                                id="scientificTopic"
                                className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm text-gray-900 ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 appearance-none cursor-pointer"
                                value={formData.scientificTopic}
                                onChange={(e) => handleInputChange("scientificTopic", e.target.value)}
                                disabled={!formData.age}
                            >
                                <option value="" disabled>Select a topic</option>
                                {formData.age &&
                                    SCIENTIFIC_TOPICS[formData.age as keyof typeof SCIENTIFIC_TOPICS]?.map((topic) => (
                                        <option key={topic.value} value={topic.value}>
                                            {topic.label}
                                        </option>
                                    ))}
                            </select>
                            <div className="absolute right-3 top-3 pointer-events-none opacity-50">
                                <svg width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M1 1L5 5L9 1" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    {/* Mission - Native Select */}
                    <div className="space-y-2">
                        <Label htmlFor="mission">Mission</Label>
                        <div className="relative">
                            <select
                                id="mission"
                                className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm text-gray-900 ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 appearance-none cursor-pointer"
                                value={formData.mission}
                                onChange={(e) => handleInputChange("mission", e.target.value)}
                                disabled={!formData.scientificTopic}
                            >
                                <option value="" disabled>Select a mission</option>
                                {formData.scientificTopic &&
                                    MISSIONS[formData.scientificTopic as keyof typeof MISSIONS]?.map((mission) => (
                                        <option key={mission.value} value={mission.value}>
                                            {mission.label}
                                        </option>
                                    ))}
                            </select>
                            <div className="absolute right-3 top-3 pointer-events-none opacity-50">
                                <svg width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M1 1L5 5L9 1" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    {/* Visual Style */}
                    <div className="space-y-2">
                        <Label>Visual Style</Label>
                        <RadioGroup
                            className="flex flex-wrap gap-4"
                            value={formData.visualStyle}
                            onValueChange={(val) => handleInputChange("visualStyle", val)}
                        >
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="cartoons" id="style-cartoons" />
                                <Label htmlFor="style-cartoons">Dibujos animados</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="watercolor" id="style-watercolor" />
                                <Label htmlFor="style-watercolor">Acuarela</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="3d_animation" id="style-3d" />
                                <Label htmlFor="style-3d">Animación 3D</Label>
                            </div>
                        </RadioGroup>
                    </div>

                    {/* Error Message */}
                    {generationError && (
                        <div className="bg-red-50 text-red-600 p-3 rounded-md flex items-center gap-2 text-sm">
                            <AlertCircle className="h-4 w-4" />
                            {generationError}
                        </div>
                    )}

                    {/* Status Message */}
                    {isGenerating && (
                        <div className="bg-blue-50 text-blue-600 p-3 rounded-md flex items-center gap-2 text-sm">
                            <Loader2 className="h-4 w-4 animate-spin" />
                            Generating your story... Status: {status}
                        </div>
                    )}

                    {/* Submit Button */}
                    <Button
                        className="w-full bg-teal-600 hover:bg-teal-700 text-lg py-6"
                        onClick={handleGenerate}
                        disabled={!isFormValid() || isGenerating}
                    >
                        {isGenerating ? (
                            <>
                                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                                Generating...
                            </>
                        ) : (
                            <>
                                <Sparkles className="mr-2 h-5 w-5" />
                                Generate Guided Story with images Async
                            </>
                        )}
                    </Button>
                </CardContent>
            </Card>

            {/* Result Viewer */}
            {storyData?.chapters && (
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <StoryViewer
                        chapters={storyData.chapters as any[]}
                        title={storyData.title || `The ${formData.protagonistName}'s Adventure`}
                    />
                </div>
            )}
        </div>
    )
}
