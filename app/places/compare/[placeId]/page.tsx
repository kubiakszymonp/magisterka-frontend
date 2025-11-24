"use client";

import { notFound } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { getPlace, getAllArticlesForPlace } from "@/lib/data";
import { ArticleTabs } from "@/components/ArticleTabs";
import { RatingCompareForm } from "@/components/RatingCompareForm";
import { Footer } from "@/components/Footer";
import { Place, Article } from "@/lib/types";

interface ComparePageProps {
  params: Promise<{ placeId: string }>;
}

export default function ComparePage({ params }: ComparePageProps) {
  const [place, setPlace] = useState<Place | null>(null);
  const [articles, setArticles] = useState<{
    adult_full: Article | null;
    adult_short: Article | null;
    child_full: Article | null;
  } | null>(null);
  const [placeId, setPlaceId] = useState<string>("");

  useEffect(() => {
    async function loadData() {
      const resolvedParams = await params;
      setPlaceId(resolvedParams.placeId);
      const placeData = await getPlace(resolvedParams.placeId);
      if (!placeData) {
        notFound();
        return;
      }
      setPlace(placeData);
      const articlesData = await getAllArticlesForPlace(resolvedParams.placeId);
      setArticles(articlesData);
    }
    loadData();
  }, [params]);

  if (!place || !articles) {
    return null;
  }

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
          ← Powrót
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
            <h1 className="text-2xl font-medium mb-1">Porównanie wersji</h1>
            <p className="text-muted-foreground text-sm">{place.name}</p>
          </div>
        </div>
      </motion.header>

      {/* Instructions */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="border-l-2 border-border pl-4 mb-10"
      >
        <p className="text-sm text-muted-foreground">
          Przeczytaj wszystkie trzy wersje przełączając się między zakładkami, 
          następnie wypełnij ankietę porównawczą.
        </p>
      </motion.section>

      {/* Tabs with articles */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.3 }}
        className="mb-12"
      >
        <ArticleTabs articles={articles} />
      </motion.section>

      {/* Compare form */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.4 }}
      >
        <RatingCompareForm placeId={placeId} />
      </motion.section>
    </main>
    <Footer />
    </>
  );
}
