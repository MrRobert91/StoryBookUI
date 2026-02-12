"use client"
import Navbar from "@/components/navbar"
import { BookOpen, Heart, Users, Sparkles, Target, Lightbulb } from "lucide-react"
import { useLanguage } from "@/components/language-context"

export default function AboutPage() {
  const { t } = useLanguage()
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <Navbar />

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            {t("about.title_1")} <span className="text-purple-600">{t("about.title_2")}</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {t("about.description")}
          </p>
        </div>

        {/* Mission Section */}
        <div className="grid md:grid-cols-2 gap-12 items-center mb-24">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">{t("about.mission_title")}</h2>
            <p className="text-lg text-gray-600 mb-6">
              {t("about.mission_desc")}
            </p>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <Target className="h-6 w-6 text-purple-600 mt-1" />
                <div>
                  <h3 className="font-semibold text-gray-900">{t("about.mission_reading_title")}</h3>
                  <p className="text-gray-600">
                    {t("about.mission_reading_desc")}
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Lightbulb className="h-6 w-6 text-purple-600 mt-1" />
                <div>
                  <h3 className="font-semibold text-gray-900">{t("about.mission_creativity_title")}</h3>
                  <p className="text-gray-600">{t("about.mission_creativity_desc")}</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Users className="h-6 w-6 text-purple-600 mt-1" />
                <div>
                  <h3 className="font-semibold text-gray-900">{t("about.mission_bonding_title")}</h3>
                  <p className="text-gray-600">
                    {t("about.mission_bonding_desc")}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <div className="text-center">
              <div className="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <BookOpen className="h-10 w-10 text-purple-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">{t("about.vision_title")}</h3>
              <p className="text-gray-600">
                {t("about.vision_desc")}
              </p>
            </div>
          </div>
        </div>

        {/* Values Section */}
        <div className="mb-24">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Our Values</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-white rounded-xl shadow-lg">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Heart className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">{t("about.value_safety_title")}</h3>
              <p className="text-gray-600">
                {t("about.value_safety_desc")}
              </p>
            </div>

            <div className="text-center p-6 bg-white rounded-xl shadow-lg">
              <div className="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Sparkles className="h-8 w-8 text-pink-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">{t("about.value_creativity_title")}</h3>
              <p className="text-gray-600">
                {t("about.value_creativity_desc")}
              </p>
            </div>

            <div className="text-center p-6 bg-white rounded-xl shadow-lg">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">{t("about.value_accessibility_title")}</h3>
              <p className="text-gray-600">
                {t("about.value_accessibility_desc")}
              </p>
            </div>
          </div>
        </div>

        {/* Product Box Section */}
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl p-12 text-center text-white">
          <h2 className="text-3xl font-bold mb-6">{t("about.offer_title")}</h2>
          <div className="grid md:grid-cols-2 gap-8 text-left">
            <div>
              <h3 className="text-xl font-semibold mb-4">{t("about.offer_list_title")}</h3>
              <ul className="space-y-2">
                <li className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4" />
                  {t("about.offer_item_1")}
                </li>
                <li className="flex items-center gap-2">
                  <BookOpen className="h-4 w-4" />
                  {t("about.offer_item_2")}
                </li>
                <li className="flex items-center gap-2">
                  <Users className="h-4 w-4" />
                  {t("about.offer_item_3")}
                </li>
                <li className="flex items-center gap-2">
                  <Heart className="h-4 w-4" />
                  {t("about.offer_item_4")}
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-4">{t("about.perfect_for_title")}</h3>
              <ul className="space-y-2">
                <li>• {t("about.perfect_item_1")}</li>
                <li>• {t("about.perfect_item_2")}</li>
                <li>• {t("about.perfect_item_3")}</li>
                <li>• {t("about.perfect_item_4")}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
