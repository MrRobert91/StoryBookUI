/** @type {import('next').NextConfig} */
const nextConfig = {
  serverExternalPackages: ['@supabase/auth-helpers-nextjs'],
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    domains: ['placeholder.svg'],
  },
}

export default nextConfig
