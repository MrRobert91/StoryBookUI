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
import { useLanguage } from "./language-context"

interface Chapter {
    title: string
    content: string
    image_url?: string
}

const SCIENTIFIC_TOPICS = {
    "3-5": [
        { value: "shapes_sizes", label: "Tamaños y formas" },
        { value: "human_body", label: "Cuerpo humano" },
        { value: "feelings", label: "Mis Sentimientos" },
        { value: "animals", label: "Animales y Naturaleza" },
        { value: "superheroes", label: "Pequeños Superhéroes" },
    ],
    "5-8": [
        { value: "sound", label: "Ciencia del Sonido" },
        { value: "water_changes", label: "Agua y Estados" },
        { value: "technology", label: "Tecnología y Robots" },
        { value: "space", label: "El Espacio Exterior" },
        { value: "cultures", label: "Culturas del Mundo" },
        { value: "mysteries", label: "Detectives y Misterios" },
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
    "feelings": [
        { value: "monster_colors", label: "El Monstruo de los Colores" },
        { value: "grumpy_cloud", label: "La Nube Gruñona" },
    ],
    "animals": [
        { value: "lost_penguin", label: "El Pingüino Perdido" },
        { value: "vet_day", label: "Veterinario por un día" },
    ],
    "superheroes": [
        { value: "everyday_hero", label: "El Héroe Cotidiano" },
        { value: "invisible_shield", label: "El Escudo Invisible" },
    ],
    "technology": [
        { value: "internet_travel", label: "Viaje al interior de la Tablet" },
        { value: "robot_friend", label: "Mi Amigo Robot" },
    ],
    "space": [
        { value: "gravity_boots", label: "Las Botas de Gravedad" },
        { value: "planet_tour", label: "Tour por los Planetas" },
    ],
    "cultures": [
        { value: "magic_passport", label: "El Pasaporte Mágico" },
        { value: "food_explorer", label: "Explorador de Sabores" },
    ],
    "mysteries": [
        { value: "museum_thief", label: "El Misterio del Museo" },
        { value: "secret_code", label: "El Código Secreto" },
    ],
}

export default function GuidedTaleGenerator() {
    const { user } = useAuth()
    const { language, t } = useLanguage()
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
        numChapters: "3",
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
            if (!supabase) throw new Error("Supabase client not initialized")
            const { data: { session } } = await supabase.auth.getSession()
            if (!session?.access_token) throw new Error("Authentication required")

            await generateStory(
                {
                    age_group: formData.age,
                    protagonist: `${formData.protagonistName}, ${formData.protagonistDesc}`,
                    scientific_topic: formData.scientificTopic,
                    mission: formData.mission,
                    visual_style: formData.visualStyle,
                    num_chapters: parseInt(formData.numChapters),
                    lang: language
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
                        {t("guided_tale.title")}
                    </CardTitle>
                    <CardDescription>{t("guided_tale.description")}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Age Selection */}
                    <div className="space-y-2">
                        <Label>{t("guided_tale.age_group")}</Label>
                        <RadioGroup
                            className="flex gap-4"
                            value={formData.age}
                            onValueChange={(val) => handleInputChange("age", val)}
                        >
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="3-5" id="age-3-5" />
                                <Label htmlFor="age-3-5">{t("guided_tale.age_3_5")}</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="5-8" id="age-5-8" />
                                <Label htmlFor="age-5-8">{t("guided_tale.age_5_8")}</Label>
                            </div>
                        </RadioGroup>
                    </div>

                    {/* Chapter Length */}
                    <div className="space-y-2">
                        <Label>{t("guided_tale.story_length")}</Label>
                        <RadioGroup
                            className="flex gap-4"
                            value={formData.numChapters}
                            onValueChange={(val) => handleInputChange("numChapters", val)}
                        >
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="3" id="chapters-3" />
                                <Label htmlFor="chapters-3">{t("guided_tale.short")}</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="6" id="chapters-6" />
                                <Label htmlFor="chapters-6">{t("guided_tale.medium")}</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="9" id="chapters-9" />
                                <Label htmlFor="chapters-9">{t("guided_tale.long")}</Label>
                            </div>
                        </RadioGroup>
                    </div>

                    {/* Protagonist */}
                    <div className="grid md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="protagonistName">{t("guided_tale.protagonist_name")}</Label>
                            <Input
                                id="protagonistName"
                                placeholder={t("guided_tale.protagonist_name_placeholder")}
                                value={formData.protagonistName}
                                onChange={(e) => handleInputChange("protagonistName", e.target.value)}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="protagonistDesc">{t("guided_tale.protagonist_desc")}</Label>
                            <Input
                                id="protagonistDesc"
                                placeholder={t("guided_tale.protagonist_desc_placeholder")}
                                value={formData.protagonistDesc}
                                onChange={(e) => handleInputChange("protagonistDesc", e.target.value)}
                            />
                        </div>
                    </div>

                    {/* Scientific Topic - Native Select */}
                    <div className="space-y-2">
                        <Label htmlFor="scientificTopic">{t("guided_tale.scientific_topic")}</Label>
                        <div className="relative">
                            <select
                                id="scientificTopic"
                                className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm text-gray-900 ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 appearance-none cursor-pointer"
                                value={formData.scientificTopic}
                                onChange={(e) => handleInputChange("scientificTopic", e.target.value)}
                                disabled={!formData.age}
                            >
                                <option value="" disabled>{t("guided_tale.select_topic")}</option>
                                {formData.age &&
                                    SCIENTIFIC_TOPICS[formData.age as keyof typeof SCIENTIFIC_TOPICS]?.map((topic) => (
                                        <option key={topic.value} value={topic.value}>
                                            {t(`guided_tale.topics.${topic.value}`)}
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
                        <Label htmlFor="mission">{t("guided_tale.mission")}</Label>
                        <div className="relative">
                            <select
                                id="mission"
                                className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm text-gray-900 ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 appearance-none cursor-pointer"
                                value={formData.mission}
                                onChange={(e) => handleInputChange("mission", e.target.value)}
                                disabled={!formData.scientificTopic}
                            >
                                <option value="" disabled>{t("guided_tale.select_mission")}</option>
                                {formData.scientificTopic &&
                                    MISSIONS[formData.scientificTopic as keyof typeof MISSIONS]?.map((mission) => (
                                        <option key={mission.value} value={mission.value}>
                                            {t(`guided_tale.missions.${mission.value}`)}
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
                        <Label>{t("guided_tale.visual_style")}</Label>
                        <RadioGroup
                            className="flex flex-wrap gap-4"
                            value={formData.visualStyle}
                            onValueChange={(val) => handleInputChange("visualStyle", val)}
                        >
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="cartoons" id="style-cartoons" />
                                <Label htmlFor="style-cartoons">{t("styles.cartoons")}</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="watercolor" id="style-watercolor" />
                                <Label htmlFor="style-watercolor">{t("styles.watercolor")}</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="3d_animation" id="style-3d" />
                                <Label htmlFor="style-3d">{t("styles.3d_animation")}</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="anime" id="style-anime" />
                                <Label htmlFor="style-anime">{t("styles.anime")}</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="child_crayons" id="style-child" />
                                <Label htmlFor="style-child">{t("styles.child_crayons")}</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="illustratio" id="style-illustratio" />
                                <Label htmlFor="style-illustratio">{t("styles.illustratio")}</Label>
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
                            {t("guided_tale.generating")} {t("guided_tale.status")}: {status}
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
                                {t("common.loading")}...
                            </>
                        ) : (
                            <>
                                <Sparkles className="mr-2 h-5 w-5" />
                                {t("guided_tale.generate_button")}
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
