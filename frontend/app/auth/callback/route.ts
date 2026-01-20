import { createServerClient } from "@supabase/ssr"
import { cookies } from "next/headers"
import { type NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get("code")

  // Robustly determine the origin for the redirect
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL
  const origin = siteUrl ? siteUrl : requestUrl.origin

  if (code) {
    const cookieStore = await cookies()
    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          getAll() {
            return cookieStore.getAll()
          },
          setAll(cookiesToSet) {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          },
        },
      }
    )

    try {
      const { error } = await supabase.auth.exchangeCodeForSession(code)
      if (!error) {
        const next = requestUrl.searchParams.get("next")
        return NextResponse.redirect(`${origin}${next || "/"}`)
      }
      console.error("Auth exchange error:", error)
    } catch (error) {
      console.error("Auth callback error:", error)
    }
  }

  // Return the user to an error page with instructions if something goes wrong
  return NextResponse.redirect(`${origin}/auth/error?message=Auth failed`)
}
