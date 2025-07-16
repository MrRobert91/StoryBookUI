import { Link } from 'react-router-dom';

export default function Navbar() {

  return (
    <nav className="bg-white border-b p-4 flex justify-between items-center">
      <div className="space-x-4">
        <Link to="/" className="font-bold">StoryBookUI</Link>
        <Link to="/make">Make a Tale</Link>
        <Link to="/about">About Us</Link>
        <Link to="/pricing">Pricing</Link>
        <Link to="/faq">FAQ</Link>
      </div>
      <div className="space-x-4 text-sm"></div>
    </nav>
  );
}
