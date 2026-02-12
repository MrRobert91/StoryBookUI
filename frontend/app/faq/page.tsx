"use client"
import Navbar from "@/components/navbar"
import FAQSection from "@/components/faq-section"
import { useLanguage } from "@/components/language-context"

export default function FAQPage() {
  const { t } = useLanguage()
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            {t("faq.title_1")} <span className="text-purple-600">{t("faq.title_2")}</span>
          </h1>
          <p className="text-xl text-gray-600">
            {t("faq.subtitle")}
          </p>
        </div>

        <FAQSection />
      </div>
    </div>
  )
}
