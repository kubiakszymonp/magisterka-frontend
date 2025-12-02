import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    // Allow all external domains without configuration
    // This disables Next.js image optimization but allows images from any domain
    unoptimized: true,
  },
};

export default nextConfig;
