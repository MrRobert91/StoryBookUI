import { Link } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';

export default function Navbar() {
  const { token } = useContext(AuthContext);

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
        {token ? (
          <Link to="/logout">Logout</Link>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
