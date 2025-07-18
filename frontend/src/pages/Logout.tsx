import { useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../services/supabase';
import { AuthContext } from '../contexts/AuthContext';

export default function Logout() {
  const navigate = useNavigate();
  const { setToken } = useContext(AuthContext);

  useEffect(() => {
    async function doLogout() {
      await supabase.auth.signOut();
      setToken(null);
      navigate('/');
    }
    doLogout();
  }, [navigate, setToken]);

  return null;
}
