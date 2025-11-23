import { createClient } from "@/lib/supabase/server"
import { type NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get("code")
  const next = searchParams.get("next") ?? "/"

  if (code) {
    const supabase = await createClient()

    try {
      const { error } = await supabase.auth.exchangeCodeForSession(code)

      if (!error) {
        console.log("Email confirmation successful")
        // Redirect to success page or dashboard
        return NextResponse.redirect(`${origin}/auth/confirmed`)
      } else {
        console.error("Email confirmation error:", error)
        return NextResponse.redirect(`${origin}/auth/error?message=${encodeURIComponent(error.message)}`)
      }
    } catch (error) {
      console.error("Email confirmation exception:", error)
      return NextResponse.redirect(`${origin}/auth/error?message=${encodeURIComponent("Confirmation failed")}`)
    }
  }

  // Return the user to an error page with instructions
  return NextResponse.redirect(`${origin}/auth/error?message=${encodeURIComponent("No confirmation code provided")}`)
}
