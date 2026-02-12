"use client"
import Navbar from "@/components/navbar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Check, Sparkles, Zap } from "lucide-react"
import Link from "next/link"
import { useLanguage } from "@/components/language-context"

export default function PricingPage() {
  const { t } = useLanguage()
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            {t("pricing.title_1")} <span className="text-purple-600">{t("pricing.title_2")}</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {t("pricing.subtitle")}
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* Free Plan */}
          <Card className="relative border-2 border-gray-200 hover:border-purple-300 transition-colors">
            <CardHeader className="text-center pb-8">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Sparkles className="h-8 w-8 text-purple-600" />
              </div>
              <CardTitle className="text-2xl font-bold">{t("pricing.free_trial_title")}</CardTitle>
              <div className="text-4xl font-bold text-gray-900 mt-4">
                $0
                <span className="text-lg font-normal text-gray-600">{t("pricing.forever")}</span>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>{t("pricing.free_item_1")}</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>{t("pricing.free_item_2")}</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>{t("pricing.free_item_3")}</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>{t("pricing.free_item_4")}</span>
                </div>
              </div>

              <div className="pt-6">
                <Link href="/auth/sign-up" className="block">
                  <Button className="w-full bg-purple-600 hover:bg-purple-700" size="lg">
                    {t("pricing.start_free")}
                  </Button>
                </Link>
              </div>

              <p className="text-sm text-gray-500 text-center">{t("pricing.free_footer")}</p>
            </CardContent>
          </Card>

          {/* Pay as You Go Plan */}
          <Card className="relative border-2 border-purple-300 hover:border-purple-400 transition-colors">
            <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-2 rounded-full text-sm font-semibold">
                {t("pricing.popular")}
              </span>
            </div>
            <CardHeader className="text-center pb-8 pt-8">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="h-8 w-8 text-purple-600" />
              </div>
              <CardTitle className="text-2xl font-bold">{t("pricing.pay_as_you_go_title")}</CardTitle>
              <div className="text-4xl font-bold text-gray-900 mt-4">
                $10
                <span className="text-lg font-normal text-gray-600">{t("pricing.stories_count")}</span>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>{t("pricing.pay_item_1")}</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>{t("pricing.pay_item_2")}</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>{t("pricing.pay_item_3")}</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>{t("pricing.pay_item_4")}</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>{t("pricing.pay_item_5")}</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>{t("pricing.pay_item_6")}</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>{t("pricing.pay_item_7")}</span>
                </div>
              </div>

              <div className="pt-6">
                <Link href="/auth/sign-up" className="block">
                  <Button
                    className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
                    size="lg"
                  >
                    {t("common.get_started")}
                  </Button>
                </Link>
              </div>

              <p className="text-sm text-gray-500 text-center">{t("pricing.pay_footer")}</p>
            </CardContent>
          </Card>
        </div>

        {/* FAQ Preview */}
        <div className="mt-24 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">{t("pricing.questions_title")}</h2>
          <p className="text-lg text-gray-600 mb-8">
            {t("pricing.questions_subtitle")}
          </p>
          <Link href="/faq">
            <Button variant="outline" size="lg">
              {t("pricing.view_faq")}
            </Button>
          </Link>
        </div>

        {/* Money Back Guarantee */}
        <div className="mt-16 bg-white rounded-2xl p-8 text-center shadow-lg">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">{t("pricing.guarantee_title")}</h3>
          <p className="text-gray-600 max-w-2xl mx-auto">
            {t("pricing.guarantee_desc")}
          </p>
        </div>
      </div>
    </div>
  )
}
