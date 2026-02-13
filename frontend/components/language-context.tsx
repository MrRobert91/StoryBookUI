"use client"

import React, { createContext, useContext, useState, useEffect } from "react"
import en from "../locales/en.json"
import es from "../locales/es.json"
import fr from "../locales/fr.json"
import pt from "../locales/pt.json"
import it from "../locales/it.json"
import de from "../locales/de.json"

type Language = "en" | "es" | "fr" | "pt" | "it" | "de"

interface LanguageContextType {
    language: Language
    setLanguage: (lang: Language) => void
    t: (key: string) => string
}

const translations: Record<string, any> = {
    en,
    es,
    fr,
    pt,
    it,
    de,
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [language, setLanguage] = useState<Language>("en")

    useEffect(() => {
        const savedLang = localStorage.getItem("language") as Language
        if (savedLang && translations[savedLang]) {
            setLanguage(savedLang)
        }
    }, [])

    const handleSetLanguage = (lang: Language) => {
        setLanguage(lang)
        localStorage.setItem("language", lang)
        document.documentElement.lang = lang
    }

    const t = (key: string) => {
        const keys = key.split(".")
        let value = translations[language]
        for (const k of keys) {
            if (value && value[k]) {
                value = value[k]
            } else {
                // Fallback to English if key missing in current language
                let fallback = translations["en"]
                for (const fk of keys) {
                    if (fallback && fallback[fk]) {
                        fallback = fallback[fk]
                    } else {
                        return key // Return the key itself if not found even in English
                    }
                }
                return fallback
            }
        }
        return typeof value === "string" ? value : key
    }

    return (
        <LanguageContext.Provider value={{ language, setLanguage: handleSetLanguage, t }}>
            {children}
        </LanguageContext.Provider>
    )
}

export const useLanguage = () => {
    const context = useContext(LanguageContext)
    if (context === undefined) {
        throw new Error("useLanguage must be used within a LanguageProvider")
    }
    return context
}
