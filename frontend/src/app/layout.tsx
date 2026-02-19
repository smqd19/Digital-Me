import type { Metadata } from "next";
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import "./globals.css";

export const metadata: Metadata = {
  title: "Qasim Sheikh | AI Engineer - Digital Avatar",
  description:
    "Talk to Qasim's AI Avatar. Senior AI Engineer with 7+ years experience in GenAI, LLMs, Voice AI, and RAG systems.",
  keywords: [
    "AI Engineer",
    "LLM",
    "GenAI",
    "Voice AI",
    "RAG",
    "Machine Learning",
    "Data Scientist",
  ],
  authors: [{ name: "Muhammad Qasim Sheikh" }],
  openGraph: {
    title: "Qasim Sheikh | AI Engineer - Digital Avatar",
    description:
      "Talk to Qasim's AI Avatar. Senior AI Engineer with 7+ years experience.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${GeistSans.variable} ${GeistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
