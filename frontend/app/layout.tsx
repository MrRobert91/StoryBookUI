import type React from "react"
import type { Metadata } from "next"
import { Geist } from "next/font/google"
import "./globals.css"
import { AuthProvider } from "@/components/auth-provider"
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server"

const geist = Geist({
  subsets: ["latin"],
})

export const metadata: Metadata = {
  title: "Supabase Auth with SSR",
  description: "A Next.js application with Supabase authentication using SSR",
    generator: 'v0.dev'
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
        <AuthProvider initialSession={initialSession}>{children}</AuthProvider>
      </body>
    </html>
  )
}
