import { createClient } from "@supabase/supabase-js"
import { createClientComponentClient } from "@supabase/auth-helpers-nextjs"
import { sessionManager } from "./session-manager"

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

// Check if Supabase environment variables are available
export const isSupabaseConfigured = !!(supabaseUrl && supabaseAnonKey)

// Rate limiting for auth operations
class RateLimiter {
  private requests: number[] = []
  private readonly maxRequests = 10 // Max 10 requests
  private readonly timeWindow = 60 * 1000 // Per minute

  canMakeRequest(): boolean {
    const now = Date.now()
    // Remove old requests outside time window
    this.requests = this.requests.filter((time) => now - time < this.timeWindow)

    if (this.requests.length >= this.maxRequests) {
      console.warn("Rate limit reached, blocking request")
      return false
    }

    this.requests.push(now)
    return true
  }
}

const rateLimiter = new RateLimiter()

// Create the raw Supabase client first
let rawSupabaseClient: any = null

// Only initialize on client side
if (typeof window !== "undefined" && isSupabaseConfigured) {
  try {
    rawSupabaseClient = createClientComponentClient()
    console.log("Supabase client initialized successfully.")
  } catch (error) {
    console.warn("Failed to initialize Supabase client:", error)
    rawSupabaseClient = null
  }
} else if (typeof window !== "undefined" && !isSupabaseConfigured) {
  console.warn("Supabase environment variables not configured. Client will not be initialized.")
}

// Enhanced Supabase client wrapper
class SupabaseClientWrapper {
  private client: any
  private isInitialized = false
  private authStateListeners = new Set()

  constructor() {
    this.client = rawSupabaseClient
    this.isInitialized = !!rawSupabaseClient
  }

  // Expose the from method for database operations
  from(table: string) {
    if (!this.client) {
      throw new Error("Supabase client not initialized")
    }
    return this.client.from(table)
  }

  // Expose the rpc method for remote procedure calls
  rpc(fn: string, args?: any) {
    if (!this.client) {
      throw new Error("Supabase client not initialized")
    }
    return this.client.rpc(fn, args)
  }

  get auth() {
    if (!this.client) return null

    return {
      signInWithPassword: async (credentials: any) => {
        if (!rateLimiter.canMakeRequest()) {
          throw new Error("Rate limit exceeded. Please wait before trying again.")
        }

        try {
          const result = await this.client.auth.signInWithPassword(credentials)
          if (result.data?.session) {
            sessionManager.updateSession(result.data.session)
          }
          return result
        } catch (error) {
          if (error instanceof Error && error.message.includes("rate limit")) {
            throw new Error("Too many login attempts. Please wait a moment and try again.")
          }
          throw error
        }
      },

      signInWithOAuth: async (credentials: any) => {
        if (!rateLimiter.canMakeRequest()) {
          throw new Error("Rate limit exceeded. Please wait before trying again.")
        }
        return await this.client.auth.signInWithOAuth(credentials)
      },

      signUp: async (credentials: any) => {
        if (!rateLimiter.canMakeRequest()) {
          throw new Error("Rate limit exceeded. Please wait before trying again.")
        }

        try {
          return await this.client.auth.signUp(credentials)
        } catch (error) {
          if (error instanceof Error && error.message.includes("rate limit")) {
            throw new Error("Too many signup attempts. Please wait a moment and try again.")
          }
          throw error
        }
      },

      signOut: async () => {
        console.log("SupabaseClientWrapper: Calling signOut. Client available:", !!this.client)
        try {
          sessionManager.clearCache()
          const result = await this.client.auth.signOut()
          console.log("SupabaseClientWrapper: signOut completed.", result)
          return result
        } catch (error) {
          console.warn("SupabaseClientWrapper: Signout error (non-critical):", error)
          return { error: null }
        }
      },

      getSession: async () => {
        if (!this.client) return { data: { session: null }, error: null }
        return await sessionManager.getSession(this.client)
      },

      getUser: async () => {
        if (!this.client) return { data: { user: null }, error: null }

        try {
          // Get user from cached session first
          const sessionResult = await this.getSession()
          if (sessionResult.data?.session?.user) {
            return { data: { user: sessionResult.data.session.user }, error: null }
          }

          // Only make API call if no cached user
          if (rateLimiter.canMakeRequest()) {
            return await this.client.auth.getUser()
          } else {
            return { data: { user: null }, error: null }
          }
        } catch (error) {
          console.warn("User fetch error (non-critical):", error)
          return { data: { user: null }, error: null }
        }
      },

      onAuthStateChange: (callback: any) => {
        if (!this.client) return { data: { subscription: null } }

        try {
          // Prevent duplicate listeners
          if (this.authStateListeners.has(callback)) {
            return { data: { subscription: null } }
          }

          this.authStateListeners.add(callback)

          const { data } = this.client.auth.onAuthStateChange((event: string, session: any) => {
            sessionManager.updateSession(session)
            callback(event, session)
          })

          // Clean up listener on unsubscribe
          const originalUnsubscribe = data.subscription.unsubscribe
          data.subscription.unsubscribe = () => {
            this.authStateListeners.delete(callback)
            originalUnsubscribe()
          }

          return { data }
        } catch (error) {
          console.warn("Auth state change error (non-critical):", error)
          return { data: { subscription: null } }
        }
      },
    }
  }

  get storage() {
    if (!this.client) {
      throw new Error("Supabase client not initialized")
    }
    return this.client.storage
  }
}

// Create the Supabase client with enhanced error handling
// Make sure it's available even for anonymous users
export const supabase = isSupabaseConfigured ? new SupabaseClientWrapper() : null

// Create an anonymous client for operations that don't require authentication
export const createAnonymousClient = () => {
  if (!isSupabaseConfigured) {
    return null
  }

  return createClient(supabaseUrl!, supabaseAnonKey!)
}

// Export a function to get a fresh client instance
export const getSupabaseClient = () => {
  if (!isSupabaseConfigured) {
    return null
  }

  return createClient(supabaseUrl!, supabaseAnonKey!)
}
