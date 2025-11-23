// Session manager with caching and throttling
class SessionManager {
  private static instance: SessionManager
  private sessionCache: any = null
  private lastFetch = 0
  private readonly CACHE_DURATION = 5 * 60 * 1000 // 5 minutes
  private readonly MIN_FETCH_INTERVAL = 10 * 1000 // 10 seconds minimum between fetches
  private isRefreshing = false
  private refreshPromise: Promise<any> | null = null

  static getInstance(): SessionManager {
    if (!SessionManager.instance) {
      SessionManager.instance = new SessionManager()
    }
    return SessionManager.instance
  }

  async getSession(supabaseClient: any): Promise<any> {
    const now = Date.now()

    // Return cached session if still valid
    if (this.sessionCache && now - this.lastFetch < this.CACHE_DURATION) {
      return { data: { session: this.sessionCache }, error: null }
    }

    // Prevent concurrent requests
    if (this.isRefreshing && this.refreshPromise) {
      return await this.refreshPromise
    }

    // Throttle requests
    if (now - this.lastFetch < this.MIN_FETCH_INTERVAL) {
      return { data: { session: this.sessionCache }, error: null }
    }

    this.isRefreshing = true
    this.refreshPromise = this.fetchSession(supabaseClient)

    try {
      const result = await this.refreshPromise
      return result
    } finally {
      this.isRefreshing = false
      this.refreshPromise = null
    }
  }

  private async fetchSession(supabaseClient: any): Promise<any> {
    try {
      const result = await supabaseClient.auth.getSession()

      if (!result.error) {
        this.sessionCache = result.data.session
        this.lastFetch = Date.now()
      }

      return result
    } catch (error) {
      console.warn("Session fetch error:", error)
      return { data: { session: null }, error }
    }
  }

  clearCache(): void {
    this.sessionCache = null
    this.lastFetch = 0
  }

  updateSession(session: any): void {
    this.sessionCache = session
    this.lastFetch = Date.now()
  }
}

export const sessionManager = SessionManager.getInstance()
