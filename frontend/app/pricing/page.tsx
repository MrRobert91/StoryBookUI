import Navbar from "@/components/navbar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Check, Sparkles, Zap } from "lucide-react"
import Link from "next/link"

export default function PricingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Simple, Transparent <span className="text-purple-600">Pricing</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Choose the perfect plan for your family's storytelling needs. Start free and upgrade anytime.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* Free Plan */}
          <Card className="relative border-2 border-gray-200 hover:border-purple-300 transition-colors">
            <CardHeader className="text-center pb-8">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Sparkles className="h-8 w-8 text-purple-600" />
              </div>
              <CardTitle className="text-2xl font-bold">Free Trial</CardTitle>
              <div className="text-4xl font-bold text-gray-900 mt-4">
                $0
                <span className="text-lg font-normal text-gray-600">/forever</span>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>1 sample story to try our magic</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Access to basic story templates</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Safe, child-friendly content</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Mobile-friendly interface</span>
                </div>
              </div>

              <div className="pt-6">
                <Link href="/auth/sign-up" className="block">
                  <Button className="w-full bg-purple-600 hover:bg-purple-700" size="lg">
                    Start Free Trial
                  </Button>
                </Link>
              </div>

              <p className="text-sm text-gray-500 text-center">Perfect for trying out Cuentee</p>
            </CardContent>
          </Card>

          {/* Pay as You Go Plan */}
          <Card className="relative border-2 border-purple-300 hover:border-purple-400 transition-colors">
            <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-2 rounded-full text-sm font-semibold">
                Most Popular
              </span>
            </div>
            <CardHeader className="text-center pb-8 pt-8">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="h-8 w-8 text-purple-600" />
              </div>
              <CardTitle className="text-2xl font-bold">Pay as You Go</CardTitle>
              <div className="text-4xl font-bold text-gray-900 mt-4">
                $10
                <span className="text-lg font-normal text-gray-600">/10 stories</span>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>10 personalized stories</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Advanced AI story generation</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Custom character creation</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Story saving & sharing</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Multiple story themes</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Priority support</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>No expiration date</span>
                </div>
              </div>

              <div className="pt-6">
                <Link href="/auth/sign-up" className="block">
                  <Button
                    className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
                    size="lg"
                  >
                    Get Started
                  </Button>
                </Link>
              </div>

              <p className="text-sm text-gray-500 text-center">Perfect for regular storytelling families</p>
            </CardContent>
          </Card>
        </div>

        {/* FAQ Preview */}
        <div className="mt-24 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Have Questions?</h2>
          <p className="text-lg text-gray-600 mb-8">
            Check out our frequently asked questions or contact our support team.
          </p>
          <Link href="/faq">
            <Button variant="outline" size="lg">
              View FAQ
            </Button>
          </Link>
        </div>

        {/* Money Back Guarantee */}
        <div className="mt-16 bg-white rounded-2xl p-8 text-center shadow-lg">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">💯 Satisfaction Guarantee</h3>
          <p className="text-gray-600 max-w-2xl mx-auto">
            We're confident you'll love Cuentee. If you're not completely satisfied with your stories, contact us
            within 30 days for a full refund. No questions asked, no commitment required.
          </p>
        </div>
      </div>
    </div>
  )
}
