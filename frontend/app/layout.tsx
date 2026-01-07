import type React from "react"
import type { Metadata } from "next"
import { Geist } from "next/font/google"
import "./globals.css"
import { AuthProvider } from "@/components/auth-provider"
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server"
import { Footer } from "@/components/footer"

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
  let initialSession = null
  if (isSupabaseConfigured) {
    try {
      const supabase = await createClient()
      const { data } = await supabase.auth.getSession()
      initialSession = data.session
    } catch (error) {
      console.warn("Error getting initial session:", error)
    }
  }

  return (
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
  )
}
