/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    PYTHON_API_URL: process.env.PYTHON_API_URL,
  },
}

module.exports = nextConfig 