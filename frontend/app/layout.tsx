import type React from "react"
import type { Metadata } from "next"
import { Geist } from "next/font/google"
import "./globals.css"
import { AuthProvider } from "@/components/auth-provider"
import { Footer } from "@/components/footer"
import { LanguageProvider } from "@/components/language-context"

const geist = Geist({
  subsets: ["latin"],
})

export const metadata: Metadata = {
  title: "Cuentee - Create Magical Stories",
  description: "A magical platform to create and share children's stories powered by AI",
  generator: 'v0.dev',
  icons: {
    icon: "/favicon.png",
  },
}

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // Get initial session for AuthProvider
  // We don't fetch on the server to avoid the "Using the user object..." warning
  // and to reduce the number of requests. The AuthProvider will hydrate the session on the client.
  const initialSession = null

  return (
    <LanguageProvider>
      <html lang="en">
        <body className={geist.className}>
          <AuthProvider initialSession={initialSession}>
            <div className="flex flex-col min-h-screen">
              <main className="flex-grow">{children}</main>
              <Footer />
            </div>
          </AuthProvider>
        </body>
      </html>
    </LanguageProvider>
  )
}
