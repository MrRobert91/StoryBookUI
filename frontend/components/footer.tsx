import Link from "next/link"

export function Footer() {
    return (
        <footer className="bg-white border-t border-gray-100 py-12 mt-auto">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex flex-col md:flex-row justify-between items-center gap-6">
                    <div className="text-gray-500 text-sm">
                        © {new Date().getFullYear()} Cuentee. All rights reserved.
                    </div>

                    <div className="flex flex-wrap justify-center gap-6 sm:gap-8">
                        <Link href="/cookie-policy" className="text-sm text-gray-500 hover:text-purple-600 transition-colors">
                            Cookie Policy
                        </Link>
                        <Link href="/privacy-policy" className="text-sm text-gray-500 hover:text-purple-600 transition-colors">
                            Privacy Policy
                        </Link>
                        <Link href="/terms-of-service" className="text-sm text-gray-500 hover:text-purple-600 transition-colors">
                            Terms of Service
                        </Link>
                    </div>
                </div>
            </div>
        </footer>
    )
}
