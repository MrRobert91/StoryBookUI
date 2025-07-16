import { createContext, useContext, useEffect, useState } from 'react';
import { createClient, SupabaseClient, Session } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string;

const supabase = createClient(supabaseUrl, supabaseAnonKey);

const SessionContext = createContext<Session | null>(null);
const SupabaseContext = createContext<SupabaseClient>(supabase);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);

  useEffect(() => {
    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });
    setSession(supabase.auth.session());
    return () => {
      listener.subscription.unsubscribe();
    };
  }, []);

  return (
    <SessionContext.Provider value={session}>
      <SupabaseContext.Provider value={supabase}>
        {children}
      </SupabaseContext.Provider>
    </SessionContext.Provider>
  );
}

export const useSession = () => useContext(SessionContext);
export const useSupabaseClient = () => useContext(SupabaseContext);
