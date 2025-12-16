import Navbar from "@/components/navbar"

export default function PrivacyPolicyPage() {
    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar />
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Privacy Policy</h1>

                <div className="prose prose-purple max-w-none bg-white p-8 rounded-lg shadow-sm">
                    <p className="mb-4">Effective Date: {new Date().toLocaleDateString()}</p>

                    <p>
                        At Cuentee, we take your privacy seriously. This Privacy Policy describes how we collect, use, and protect your personal information.
                    </p>

                    <h2 className="text-xl font-semibold mt-6 mb-4">1. Information We Collect</h2>
                    <p>We collect information you provide directly to us, such as:</p>
                    <ul className="list-disc pl-6 mb-4 space-y-2">
                        <li>Account information (email address, password).</li>
                        <li>Content you create (stories, prompts, images).</li>
                        <li>Usage data (how you interact with our service).</li>
                    </ul>

                    <h2 className="text-xl font-semibold mt-6 mb-4">2. How We Use Your Information</h2>
                    <p>We use your information to:</p>
                    <ul className="list-disc pl-6 mb-4 space-y-2">
                        <li>Provide, maintain, and improve our services.</li>
                        <li>Generate personalized stories and images using AI models.</li>
                        <li>Communicate with you about products, services, offers, and events.</li>
                    </ul>

                    <h2 className="text-xl font-semibold mt-6 mb-4">3. Data Security</h2>
                    <p>
                        We use appropriate technical and organizational measures to protect your personal information against unauthorized processing, loss, destruction, or damage.
                    </p>

                    <h2 className="text-xl font-semibold mt-6 mb-4">4. Third-Party Services</h2>
                    <p>
                        We use third-party AI providers (like OpenAI and Groq) to generate content. We do not share your personal contact information with these providers,
                        only the prompts necessary to generate your stories.
                    </p>

                    <h2 className="text-xl font-semibold mt-6 mb-4">5. Contact Us</h2>
                    <p>
                        If you have any questions about this Privacy Policy, please contact us support@cuentee.com.
                    </p>
                </div>
            </div>
        </div>
    )
}
