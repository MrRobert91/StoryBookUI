import { createBrowserClient } from "@supabase/ssr"

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

// Check if Supabase environment variables are available
export const isSupabaseConfigured = !!(supabaseUrl && supabaseAnonKey)

// Create a single browser-side supabase instance
export const supabase = isSupabaseConfigured
  ? createBrowserClient(supabaseUrl!, supabaseAnonKey!)
  : null

// Export a function to get a fresh client instance if needed
export const getSupabaseClient = () => {
  if (!isSupabaseConfigured) return null
  return createBrowserClient(supabaseUrl!, supabaseAnonKey!)
}

// For backward compatibility and specialized use cases
export const createAnonymousClient = () => getSupabaseClient()
