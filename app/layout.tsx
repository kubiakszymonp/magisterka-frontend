import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { VoiceProvider } from "@/lib/voice-context";
import { ScrollToTop } from "@/components/ScrollToTop";

const inter = Inter({
  variable: "--font-geist-sans",
  subsets: ["latin", "latin-ext"],
});

export const metadata: Metadata = {
  title: "Badanie przewodników turystycznych",
  description: "Porównanie różnych wersji przewodników turystycznych",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pl">
      <body className={`${inter.variable} font-sans antialiased min-h-screen bg-background flex flex-col`}>
        <VoiceProvider>
          <ScrollToTop />
          <div className="flex-1">
            {children}
          </div>
        </VoiceProvider>
      </body>
    </html>
  );
}
