import Navbar from "@/components/navbar"
import { BookOpen, Heart, Users, Sparkles, Target, Lightbulb } from "lucide-react"

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <Navbar />

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            About <span className="text-purple-600">Cuentee</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            We believe every child deserves magical stories that spark imagination, foster creativity, and create
            unforgettable bonding moments with their families.
          </p>
        </div>

        {/* Mission Section */}
        <div className="grid md:grid-cols-2 gap-12 items-center mb-24">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Mission</h2>
            <p className="text-lg text-gray-600 mb-6">
              We want to create an accessible and simple platform where parents, educators, and children can generate
              personalized stories using artificial intelligence. Our purpose is to foster creativity, reading habits,
              and fun in children, offering a safe, fast, and easy-to-use environment.
            </p>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <Target className="h-6 w-6 text-purple-600 mt-1" />
                <div>
                  <h3 className="font-semibold text-gray-900">Promote Early Reading</h3>
                  <p className="text-gray-600">
                    Encourage reading habits from an early age through engaging, personalized content.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Lightbulb className="h-6 w-6 text-purple-600 mt-1" />
                <div>
                  <h3 className="font-semibold text-gray-900">Instant Creativity</h3>
                  <p className="text-gray-600">Provide an accessible solution to create unique stories instantly.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Users className="h-6 w-6 text-purple-600 mt-1" />
                <div>
                  <h3 className="font-semibold text-gray-900">Family Bonding</h3>
                  <p className="text-gray-600">
                    Create magical moments and strengthen family connections through storytelling.
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
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Our Vision</h3>
              <p className="text-gray-600">
                To become the go-to platform for creative storytelling, where every family can access personalized,
                educational, and entertaining content that grows with their children.
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
              <h3 className="text-xl font-semibold mb-3">Safety First</h3>
              <p className="text-gray-600">
                All our content is carefully designed to be age-appropriate, educational, and safe for children.
              </p>
            </div>

            <div className="text-center p-6 bg-white rounded-xl shadow-lg">
              <div className="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Sparkles className="h-8 w-8 text-pink-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Creativity</h3>
              <p className="text-gray-600">
                We believe in the power of imagination and strive to inspire creativity in every story we help create.
              </p>
            </div>

            <div className="text-center p-6 bg-white rounded-xl shadow-lg">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Accessibility</h3>
              <p className="text-gray-600">
                Our platform is designed to be simple, intuitive, and accessible to families from all backgrounds.
              </p>
            </div>
          </div>
        </div>

        {/* Product Box Section */}
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl p-12 text-center text-white">
          <h2 className="text-3xl font-bold mb-6">🎁 "Magical Tales at Your Fingertips!"</h2>
          <div className="grid md:grid-cols-2 gap-8 text-left">
            <div>
              <h3 className="text-xl font-semibold mb-4">What We Offer:</h3>
              <ul className="space-y-2">
                <li className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4" />
                  Create unique and personalized stories for your children
                </li>
                <li className="flex items-center gap-2">
                  <BookOpen className="h-4 w-4" />
                  Generate adventure-filled stories with just one click
                </li>
                <li className="flex items-center gap-2">
                  <Users className="h-4 w-4" />
                  Fun interface designed for the whole family
                </li>
                <li className="flex items-center gap-2">
                  <Heart className="h-4 w-4" />
                  No downloads needed: everything from your browser
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-4">Perfect For:</h3>
              <ul className="space-y-2">
                <li>• Busy parents seeking quality bonding time</li>
                <li>• Creative educators looking for engaging content</li>
                <li>• Families who love bedtime stories</li>
                <li>• Anyone wanting to inspire young imaginations</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
