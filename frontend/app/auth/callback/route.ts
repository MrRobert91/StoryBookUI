import { createRouteHandlerClient } from "@supabase/auth-helpers-nextjs"
import { cookies } from "next/headers"
import { type NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get("code")

  // Robustly determine the origin for the redirect
  // 1. Prefer NEXT_PUBLIC_SITE_URL if configured
  // 2. Fallback to the requested origin (works for local dev)
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL
  const origin = siteUrl ? siteUrl : requestUrl.origin

  if (code) {
    const cookieStore = cookies()
    const supabase = createRouteHandlerClient({ cookies: () => cookieStore })

    try {
      await supabase.auth.exchangeCodeForSession(code)
      return NextResponse.redirect(`${origin}/auth/confirmed`)
    } catch (error) {
      console.error("Auth callback error:", error)
      return NextResponse.redirect(`${origin}/auth/error?message=Auth failed`)
    }
  }

  // Return the user to an error page with instructions
  return NextResponse.redirect(`${origin}/auth/error?message=No code provided`)
}
