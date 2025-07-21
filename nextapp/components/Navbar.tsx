'use client';
import Link from 'next/link';
import { useAuth } from '../lib/auth-context';

export default function Navbar() {
  const { user, login, logout } = useAuth();

  return (
    <nav className="bg-white border-b p-4 flex justify-between items-center">
      <div className="space-x-4">
        <Link href="/" className="font-bold">StoryBookUI</Link>
        <Link href="/make" className="hover:underline">Make a Tale</Link>
        <Link href="/about" className="hover:underline">About Us</Link>
        <Link href="/pricing" className="hover:underline">Pricing</Link>
        <Link href="/faq" className="hover:underline">FAQ</Link>
      </div>
      <div className="space-x-4 text-sm">
        {user ? (
          <>
            <span className="mr-2">Hola, {user}</span>
            <button onClick={logout} className="hover:underline">Logout</button>
          </>
        ) : (
          <>
            <button onClick={() => login('demo')} className="hover:underline">Login</button>
            <Link href="#" className="hover:underline">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
