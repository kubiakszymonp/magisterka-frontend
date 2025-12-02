"use client";

import { notFound } from "next/navigation";
import { useEffect, useState, useMemo, useRef } from "react";
import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { getPlace, getArticle } from "@/lib/data";
import { RatingSingleForm } from "@/components/RatingSingleForm";
import { TextToSpeech, TextToSpeechRef, getSentenceBoundaries } from "@/components/TextToSpeech";
import { Footer } from "@/components/Footer";
import { Place, Article } from "@/lib/types";

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

  // Get sentence boundaries for highlighting
  const sentenceBoundaries = useMemo(() => {
    if (!article) return [];
    return getSentenceBoundaries(article.content);
  }, [article]);

  const handleSentenceClick = (sentenceIndex: number) => {
    textToSpeechRef.current?.playFromSentence(sentenceIndex);
  };

  if (!place || !article) {
    return null;
  }

  // Render text with sentence highlighting
  const renderHighlightedText = () => {
    let lastEnd = 0;
    const elements: React.ReactNode[] = [];

    sentenceBoundaries.forEach((boundary, index) => {
      // Add any text before this sentence (whitespace, etc.)
      if (boundary.start > lastEnd) {
        elements.push(
          <span key={`gap-${index}`}>
            {article.content.slice(lastEnd, boundary.start)}
          </span>
        );
      }

      const isHighlighted = currentSentenceIndex === index;
      elements.push(
        <span
          key={`sentence-${index}`}
          onClick={() => handleSentenceClick(index)}
          className={`cursor-pointer rounded px-1 transition-all duration-200 ${
            isHighlighted 
              ? "bg-primary/15 text-foreground border-b-2 border-primary/40" 
              : "hover:bg-muted/50"
          }`}
        >
          {boundary.text}
        </span>
      );

      lastEnd = boundary.end;
    });

    // Add any remaining text
    if (lastEnd < article.content.length) {
      elements.push(
        <span key="end">{article.content.slice(lastEnd)}</span>
      );
    }

    return elements;
  };

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
              text={article.content} 
              title={article.title}
              onSentenceChange={setCurrentSentenceIndex}
            />
          </div>
          <div className="text-sm leading-relaxed text-muted-foreground select-none whitespace-pre-wrap">
            {renderHighlightedText()}
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
