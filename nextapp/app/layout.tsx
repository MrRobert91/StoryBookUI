import type { Metadata } from 'next';
import '../app/globals.css';
import Navbar from '../components/Navbar';
import { AuthProvider } from '../lib/auth-context';

export const metadata: Metadata = {
  title: 'StoryBookUI',
  description: 'Generate personalized tales with AI',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <Navbar />
          <main className="p-4 min-h-screen">{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}
