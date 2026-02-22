const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    unoptimized: true,
  },
  experimental: {
    // Allow reading content from parent directory
    outputFileTracingRoot: path.join(__dirname, '..'),
  },
};

module.exports = nextConfig;
