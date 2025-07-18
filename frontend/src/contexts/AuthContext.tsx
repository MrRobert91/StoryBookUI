import React, { createContext, useState, useEffect, ReactNode } from 'react';

interface AuthContextType {
  token: string | null;
  setToken: (token: string | null) => void;
}

export const AuthContext = createContext<AuthContextType>({
  token: null,
  setToken: () => {},
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [tokenState, setTokenState] = useState<string | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem('token');
    if (stored) {
      setTokenState(stored);
    }
  }, []);

  const setToken = (tok: string | null) => {
    if (tok) {
      localStorage.setItem('token', tok);
    } else {
      localStorage.removeItem('token');
    }
    setTokenState(tok);
  };

  return (
    <AuthContext.Provider value={{ token: tokenState, setToken }}>
      {children}
    </AuthContext.Provider>
  );
};
