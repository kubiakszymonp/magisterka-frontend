"use client";

import { notFound } from "next/navigation";
import { useEffect, useState, useRef } from "react";
import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { getPlace, getArticle } from "@/lib/data";
import { RatingSingleForm } from "@/components/RatingSingleForm";
import { TextToSpeech, TextToSpeechRef } from "@/components/TextToSpeech";
import { Footer } from "@/components/Footer";
import { Place, Article } from "@/lib/types";
import { HighlightedHtml, stripMarkdown } from "@/utils/highlightedHtml";

interface ArticlePageProps {
  params: Promise<{ placeId: string; style: string }>;
}

const styleLabels: Record<string, string> = {
  adult_full: "Dorośli – pełny",
  adult_short: "Dorośli – skrót",
  child_short: "Dzieci – skrót",
};

export default function ArticlePage({ params }: ArticlePageProps) {
  const [place, setPlace] = useState<Place | null>(null);
  const [article, setArticle] = useState<Article | null>(null);
  const [placeId, setPlaceId] = useState<string>("");
  const [style, setStyle] = useState<string>("");
  const [currentSentenceIndex, setCurrentSentenceIndex] = useState<number | null>(null);
  const textToSpeechRef = useRef<TextToSpeechRef>(null);

  useEffect(() => {
    async function loadData() {
      const resolvedParams = await params;
      setPlaceId(resolvedParams.placeId);
      setStyle(resolvedParams.style);
      const placeData = await getPlace(resolvedParams.placeId);
      const articleData = await getArticle(resolvedParams.placeId, resolvedParams.style);
      
      if (!placeData || !articleData) {
        notFound();
        return;
      }
      
      setPlace(placeData);
      setArticle(articleData);
    }
    loadData();
  }, [params]);

  const handleSentenceClick = (sentenceIndex: number) => {
    textToSpeechRef.current?.playFromSentence(sentenceIndex);
  };

  if (!place || !article) {
    return null;
  }

  // Get plain text for TextToSpeech (strip markdown formatting)
  const plainTextContent = stripMarkdown(article.content);

  return (
    <>
    <main className="container mx-auto px-4 py-16 max-w-3xl">
      {/* Back link */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Link 
          href={`/places/${placeId}`}
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-8 transition-colors"
        >
          ← Powrót do {place.name}
        </Link>
      </motion.div>

      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="mb-10"
      >
        <div className="flex flex-col md:flex-row gap-6 items-start">
          <div className="relative w-full md:w-48 h-48 md:h-48 flex-shrink-0 rounded-md overflow-hidden border border-border bg-muted/30">
            <Image
              src={place.thumbnail}
              alt={place.name}
              fill
              className="object-contain p-4"
              priority
            />
          </div>
          <div className="flex-1">
            <div className="mb-4">
              <span className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                {styleLabels[style] || style}
              </span>
            </div>
            <h1 className="text-2xl font-medium mb-2">{article.title}</h1>
            <p className="text-muted-foreground text-sm">{place.name}</p>
          </div>
        </div>
      </motion.header>

      {/* Article content */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="mb-12"
      >
        <div className="bg-card border border-border rounded-md p-6 shadow-sm">
          <div className="mb-4">
            <TextToSpeech 
              ref={textToSpeechRef}
              text={plainTextContent} 
              title={article.title}
              onSentenceChange={setCurrentSentenceIndex}
            />
          </div>
          <div className="text-sm leading-relaxed text-muted-foreground select-none prose-headings:text-foreground">
            <HighlightedHtml
              markdown={article.content}
              currentSentenceIndex={currentSentenceIndex}
              onSentenceClick={handleSentenceClick}
            />
          </div>
        </div>
      </motion.section>

      {/* Rating form */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.4 }}
        className="border-t border-border pt-8"
      >
        <RatingSingleForm
          placeId={article.placeId}
          articleStyle={article.style}
        />
      </motion.section>
    </main>
    <Footer />
    </>
  );
}
