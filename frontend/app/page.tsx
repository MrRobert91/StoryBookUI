"use client"
import { Button } from "@/components/ui/button"
import { Sparkles, BookOpen, Users } from "lucide-react"
import Navbar from "@/components/navbar"
import Link from "next/link"
import { useLanguage } from "@/components/language-context"

export default function Home() {
  const { t } = useLanguage()
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <Navbar />

      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              ✨ {t("home.hero_title_1")} <span className="text-purple-600">{t("home.hero_title_2")}</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              {t("home.hero_description")}
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/make-tale">
                <Button size="lg" className="bg-purple-600 hover:bg-purple-700 text-lg px-8 py-4">
                  <Sparkles className="mr-2 h-5 w-5" />
                  {t("home.cta_button")}
                </Button>
              </Link>
              <Link href="/about">
                <Button size="lg" variant="outline" className="text-lg px-8 py-4 bg-transparent">
                  {t("home.learn_more")}
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">{t("home.why_choose_title")}</h2>
            <p className="text-lg text-gray-600">{t("home.why_choose_subtitle")}</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Sparkles className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">{t("home.feature_ai_title")}</h3>
              <p className="text-gray-600">{t("home.feature_ai_desc")}</p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <BookOpen className="h-8 w-8 text-pink-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">{t("home.feature_personalized_title")}</h3>
              <p className="text-gray-600">{t("home.feature_personalized_desc")}</p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">{t("home.feature_family_title")}</h3>
              <p className="text-gray-600">{t("home.feature_family_desc")}</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-24 bg-gradient-to-r from-purple-600 to-pink-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-white mb-4">{t("home.cta_ready_title")}</h2>
          <p className="text-xl text-purple-100 mb-8">
            {t("home.cta_ready_subtitle")}
          </p>
          <Link href="/auth/sign-up">
            <Button size="lg" className="bg-white text-purple-600 hover:bg-gray-100 text-lg px-8 py-4">
              {t("home.cta_trial_button")}
            </Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
