/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    AUTH0_CLIENT_ID: process.env.AUTH0_CLIENT_ID,
    AUTH0_URL: process.env.AUTH0_URL,
    AUTH0_AUDIENCE: process.env.AUTH0_AUDIENCE,
  },
};

module.exports = nextConfig;
