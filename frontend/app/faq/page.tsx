import Navbar from "@/components/navbar"
import FAQSection from "@/components/faq-section"

export default function FAQPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Frequently Asked <span className="text-purple-600">Questions</span>
          </h1>
          <p className="text-xl text-gray-600">
            Everything you need to know about Cuentee and creating magical stories.
          </p>
        </div>

        <FAQSection />
      </div>
    </div>
  )
}
