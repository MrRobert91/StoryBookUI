import { createServerComponentClient } from "@supabase/auth-helpers-nextjs"
import { cache } from "react"

// Check if Supabase environment variables are available
export const isSupabaseConfigured =
  typeof process.env.NEXT_PUBLIC_SUPABASE_URL === "string" &&
  process.env.NEXT_PUBLIC_SUPABASE_URL.length > 0 &&
  typeof process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY === "string" &&
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY.length > 0

// Reduce server-side cache duration for better session sync
const serverSessionCache = new Map<string, { session: any; timestamp: number }>()
const CACHE_DURATION = 30 * 1000 // Reduced to 30 seconds

// Create a cached version of the Supabase client for Server Components
export const createClient = cache(async () => {
  if (!isSupabaseConfigured) {
    console.warn("Supabase not configured, returning mock client")
    return {
      auth: {
        getUser: () => Promise.resolve({ data: { user: null }, error: null }),
        getSession: () => Promise.resolve({ data: { session: null }, error: null }),
        signInWithPassword: () => Promise.resolve({ data: null, error: new Error("Supabase not configured") }),
        signUp: () => Promise.resolve({ data: null, error: new Error("Supabase not configured") }),
        signOut: () => Promise.resolve({ error: new Error("Supabase not configured") }),
      },
      from: (table: string) => ({
        select: () => Promise.resolve({ data: [], error: null }),
        insert: () => Promise.resolve({ data: null, error: new Error("Supabase not configured") }),
        delete: () => Promise.resolve({ error: new Error("Supabase not configured") }),
        eq: () => ({
          order: () => Promise.resolve({ data: [], error: null }),
          single: () => Promise.resolve({ data: null, error: new Error("Supabase not configured") }),
        }),
        order: () => Promise.resolve({ data: [], error: null }),
      }),
    }
  }

  try {
    // Check if we're in a server environment
    if (typeof window !== "undefined") {
      console.warn("Server client called on client side, returning mock")
      return {
        auth: {
          getUser: () => Promise.resolve({ data: { user: null }, error: null }),
          getSession: () => Promise.resolve({ data: { session: null }, error: null }),
          signInWithPassword: () => Promise.resolve({ data: null, error: new Error("Use client-side auth") }),
          signUp: () => Promise.resolve({ data: null, error: new Error("Use client-side auth") }),
          signOut: () => Promise.resolve({ error: new Error("Use client-side auth") }),
        },
        from: (table: string) => ({
          select: () => Promise.resolve({ data: [], error: null }),
          insert: () => Promise.resolve({ data: null, error: new Error("Use client-side operations") }),
          delete: () => Promise.resolve({ error: new Error("Use client-side operations") }),
          eq: () => ({
            order: () => Promise.resolve({ data: [], error: null }),
            single: () => Promise.resolve({ data: null, error: new Error("Use client-side operations") }),
          }),
          order: () => Promise.resolve({ data: [], error: null }),
        }),
      }
    }

    // Dynamic import for server-side only
    const { cookies } = await import("next/headers")
    const cookieStore = cookies()
    const client = createServerComponentClient({ cookies: () => cookieStore })

    // Generate cache key from cookies
    const cookieString = cookieStore.toString()
    const cacheKey = Buffer.from(cookieString).toString("base64").slice(0, 32)

    return {
      // Expose the full client for database operations
      ...client,
      auth: {
        getUser: async () => {
          try {
            // For better session sync, reduce cache usage
            const cached = serverSessionCache.get(cacheKey)
            const now = Date.now()

            if (cached && now - cached.timestamp < CACHE_DURATION) {
              return { data: { user: cached.session?.user || null }, error: null }
            }

            const result = await client.auth.getUser()

            // Cache the result only if successful
            if (result.data?.user && !result.error) {
              serverSessionCache.set(cacheKey, {
                session: { user: result.data.user },
                timestamp: now,
              })
            } else {
              // Clear cache if no user
              serverSessionCache.delete(cacheKey)
            }

            return result
          } catch (error) {
            console.warn("Server getUser error:", error)
            return { data: { user: null }, error: error }
          }
        },

        getSession: async () => {
          try {
            // For better session sync, reduce cache usage
            const cached = serverSessionCache.get(cacheKey)
            const now = Date.now()

            if (cached && now - cached.timestamp < CACHE_DURATION) {
              return { data: { session: cached.session }, error: null }
            }

            const result = await client.auth.getSession()

            // Cache the result only if successful
            if (result.data?.session && !result.error) {
              serverSessionCache.set(cacheKey, {
                session: result.data.session,
                timestamp: now,
              })
            } else {
              // Clear cache if no session
              serverSessionCache.delete(cacheKey)
            }

            return result
          } catch (error) {
            console.warn("Server getSession error:", error)
            return { data: { session: null }, error: error }
          }
        },

        // Pass through other auth methods
        signInWithPassword: (credentials: any) => client.auth.signInWithPassword(credentials),
        signUp: (credentials: any) => client.auth.signUp(credentials),
        signOut: () => client.auth.signOut(),
      },
    }
  } catch (error) {
    console.error("Error creating server Supabase client:", error)
    return {
      auth: {
        getUser: () => Promise.resolve({ data: { user: null }, error: error }),
        getSession: () => Promise.resolve({ data: { session: null }, error: error }),
        signInWithPassword: () => Promise.resolve({ data: null, error: error }),
        signUp: () => Promise.resolve({ data: null, error: error }),
        signOut: () => Promise.resolve({ error: error }),
      },
      from: (table: string) => ({
        select: () => Promise.resolve({ data: [], error: error }),
        insert: () => Promise.resolve({ data: null, error: error }),
        delete: () => Promise.resolve({ error: error }),
        eq: () => ({
          order: () => Promise.resolve({ data: [], error: error }),
          single: () => Promise.resolve({ data: null, error: error }),
        }),
        order: () => Promise.resolve({ data: [], error: error }),
      }),
    }
  }
})

// Clean up old cache entries more frequently
if (typeof global !== "undefined" && typeof setInterval !== "undefined") {
  setInterval(() => {
    const now = Date.now()
    for (const [key, value] of serverSessionCache.entries()) {
      if (now - value.timestamp > CACHE_DURATION) {
        serverSessionCache.delete(key)
      }
    }
  }, CACHE_DURATION / 2) // Clean up every 15 seconds
}
