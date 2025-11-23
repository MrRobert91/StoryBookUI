import { createMiddlewareClient } from "@supabase/auth-helpers-nextjs"
import { NextResponse, type NextRequest } from "next/server"

// Check if Supabase environment variables are available
export const isSupabaseConfigured =
  typeof process.env.NEXT_PUBLIC_SUPABASE_URL === "string" &&
  process.env.NEXT_PUBLIC_SUPABASE_URL.length > 0 &&
  typeof process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY === "string" &&
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY.length > 0

export async function updateSession(request: NextRequest) {
  // If Supabase is not configured, just continue without auth
  if (!isSupabaseConfigured) {
    return NextResponse.next({ request })
  }

  const res = NextResponse.next()

  try {
    // Create a Supabase client configured to use cookies
    const supabase = createMiddlewareClient({ req: request, res })

    // Check if this is an auth callback
    const requestUrl = new URL(request.url)
    const code = requestUrl.searchParams.get("code")

    if (code) {
      try {
        await supabase.auth.exchangeCodeForSession(code)
        return NextResponse.redirect(new URL("/", request.url))
      } catch (error) {
        console.warn("Auth callback error:", error)
        return NextResponse.redirect(new URL("/auth/login", request.url))
      }
    }

    // For client-side routing, we don't need to protect routes in middleware
    // The client components will handle authentication checks
    return res
  } catch (error) {
    console.warn("Middleware error:", error)
    return NextResponse.next({ request })
  }
}
