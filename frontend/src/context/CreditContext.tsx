import { createContext, useContext, useState, useEffect } from 'react';
import { useSupabaseClient, useSession } from './AuthContext';

const CreditContext = createContext<number>(0);

export function CreditProvider({ children }: { children: React.ReactNode }) {
  const supabase = useSupabaseClient();
  const session = useSession();
  const [credits, setCredits] = useState(0);

  useEffect(() => {
    async function loadCredits() {
      if (!session) {
        setCredits(0);
        return;
      }
      const { data } = await supabase
        .from('user_credits')
        .select('credits')
        .eq('id', session.user.id)
        .single();
      if (data) setCredits(data.credits);
    }
    loadCredits();
  }, [session, supabase]);

  return (
    <CreditContext.Provider value={credits}>{children}</CreditContext.Provider>
  );
}

export const useCredits = () => useContext(CreditContext);
