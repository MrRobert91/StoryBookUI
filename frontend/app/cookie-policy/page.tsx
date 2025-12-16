import Navbar from "@/components/navbar"

export default function CookiePolicyPage() {
    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar />
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Cookie Policy</h1>

                <div className="prose prose-purple max-w-none bg-white p-8 rounded-lg shadow-sm">
                    <p className="mb-4">Effective Date: {new Date().toLocaleDateString()}</p>

                    <h2 className="text-xl font-semibold mt-6 mb-4">1. What are cookies?</h2>
                    <p>
                        Cookies are small text files that are placed on your computer or mobile device when you visit a website.
                        They are widely used to make websites work more efficiently and provide information to the owners of the site.
                    </p>

                    <h2 className="text-xl font-semibold mt-6 mb-4">2. How we use cookies</h2>
                    <p>
                        We use cookies to:
                    </p>
                    <ul className="list-disc pl-6 mb-4 space-y-2">
                        <li>Keep you signed in to your account (Authentication cookies).</li>
                        <li>Remember your preferences and settings.</li>
                        <li>Understand how you use our service to improve your experience.</li>
                    </ul>

                    <h2 className="text-xl font-semibold mt-6 mb-4">3. Types of cookies we use</h2>
                    <div className="space-y-4">
                        <div>
                            <h3 className="font-medium">Essential Cookies</h3>
                            <p>These are necessary for the website to function properly. For example, we use cookies from Supabase to manage your secure login session.</p>
                        </div>
                        <div>
                            <h3 className="font-medium">Analytics Cookies</h3>
                            <p>These help us understand how visitors interact with our website by collecting and reporting information anonymously.</p>
                        </div>
                    </div>

                    <h2 className="text-xl font-semibold mt-6 mb-4">4. Managing cookies</h2>
                    <p>
                        Most web browsers allow you to control cookies through their settings preferences. However, if you limit the ability of websites to set cookies,
                        you may worsen your overall user experience, since it will no longer be personalized to you. It may also stop you from saving customized settings like login information.
                    </p>
                </div>
            </div>
        </div>
    )
}
