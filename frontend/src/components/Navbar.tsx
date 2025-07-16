import { Link } from 'react-router-dom';
import { useSession, useSupabaseClient } from '../context/AuthContext';
import { useCredits } from '../context/CreditContext';

export default function Navbar() {
  const supabase = useSupabaseClient();
  const session = useSession();
  const credits = useCredits();

  async function signIn() {
    await supabase.auth.signInWithOAuth({ provider: 'google' });
  }

  async function signOut() {
    await supabase.auth.signOut();
  }

  return (
    <nav className="bg-white border-b p-4 flex justify-between items-center">
      <div className="space-x-4">
        <Link to="/" className="font-bold">StoryBookUI</Link>
        <Link to="/make">Make a Tale</Link>
        <Link to="/about">About Us</Link>
        <Link to="/pricing">Pricing</Link>
        <Link to="/faq">FAQ</Link>
      </div>
      <div className="space-x-4 text-sm">
        {session && <span>Credits: {credits}</span>}
        {session ? (
          <button onClick={signOut}>Logout</button>
        ) : (
          <button onClick={signIn}>Login</button>
        )}
      </div>
    </nav>
  );
}
