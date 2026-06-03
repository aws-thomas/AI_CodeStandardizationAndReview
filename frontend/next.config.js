/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // API backend URL for development
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
}

module.exports = nextConfig

// Made with Bob
