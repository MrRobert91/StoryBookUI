"use client"

import { createContext, useContext, useEffect, useState, type ReactNode } from "react"
import { supabase, isSupabaseConfigured } from "@/lib/supabase/client"
// No importamos useRouter aquí, el AuthProvider solo gestiona el estado, no las redirecciones

interface AuthContextType {
  session: any
  user: any
  loading: boolean
  refreshSession: () => Promise<void>
}

const AuthContext = createContext<AuthContextType>({
  session: null,
  user: null,
  loading: true,
  refreshSession: async () => {},
})

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
  initialSession?: any
}

export function AuthProvider({ children, initialSession = null }: AuthProviderProps) {
  const [session, setSession] = useState(initialSession)
  const [loading, setLoading] = useState(!initialSession)

  const refreshSession = async () => {
    if (!isSupabaseConfigured || !supabase) return

    try {
      const { data, error } = await supabase.auth.getSession()
      if (!error && data.session) {
        setSession(data.session)
      } else {
        setSession(null)
      }
    } catch (error) {
      console.warn("Error refreshing session:", error)
      setSession(null)
    }
  }

  useEffect(() => {
    if (!isSupabaseConfigured || !supabase) {
      setLoading(false)
      return
    }

    // Get initial session only if we don't have one
    if (!initialSession) {
      refreshSession().finally(() => setLoading(false))
    } else {
      setLoading(false)
    }

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange(async (event, session) => {
      console.log("Auth state changed:", event, session?.user?.email)
      setSession(session)
      setLoading(false)

      // El AuthProvider solo actualiza el estado, no redirige.
      // Las redirecciones se manejan en los componentes de formulario o páginas protegidas.
    })

    return () => {
      subscription?.unsubscribe()
    }
  }, [initialSession]) // Dependencias ajustadas

  const value = {
    session,
    user: session?.user || null,
    loading,
    refreshSession,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
