"use client";

import { notFound } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { getPlace, getAllArticlesForPlace } from "@/lib/data";
import { ArticleCard } from "@/components/ArticleCard";
import { Button } from "@/components/ui/button";
import { Place, Article } from "@/lib/types";

interface PlacePageProps {
  params: Promise<{ placeId: string }>;
}

export default function PlacePage({ params }: PlacePageProps) {
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
      const placeData = getPlace(resolvedParams.placeId);
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

  const articleConfigs = [
    { key: "adult_full", label: "Dorośli – pełny", icon: "1", article: articles.adult_full },
    { key: "adult_short", label: "Dorośli – skrót", icon: "2", article: articles.adult_short },
    { key: "child_full", label: "Dzieci – pełny", icon: "3", article: articles.child_full },
  ];

  return (
    <main className="container mx-auto px-4 py-16 max-w-4xl">
      {/* Back link */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Link 
          href="/" 
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-8 transition-colors"
        >
          ← Powrót
        </Link>
      </motion.div>

      {/* Place header */}
      <motion.header
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="mb-12"
      >
        <div className="relative h-48 w-full rounded-md overflow-hidden bg-muted mb-6 shadow-md">
          <Image
            src={place.thumbnail}
            alt={place.name}
            fill
            className="object-cover"
            priority
          />
        </div>
        <h1 className="text-2xl font-medium mb-2">{place.name}</h1>
        <p className="text-muted-foreground text-sm">{place.description}</p>
      </motion.header>

      {/* Articles section */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="mb-12"
      >
        <h2 className="text-sm font-medium uppercase tracking-wider text-muted-foreground mb-6">
          Wersje przewodnika
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {articleConfigs.map((config, index) =>
            config.article ? (
              <ArticleCard
                key={config.key}
                article={config.article}
                label={config.label}
                icon={config.icon}
                index={index}
              />
            ) : (
              <motion.div
                key={config.key}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="rounded-md border border-dashed border-border p-4 text-center text-muted-foreground text-sm shadow-sm"
              >
                {config.label}
                <br />
                <span className="text-xs">Niedostępny</span>
              </motion.div>
            )
          )}
        </div>
      </motion.section>

      {/* Compare section */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.3 }}
        className="border-t border-border pt-8"
      >
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-medium mb-1">Porównaj wersje</h2>
            <p className="text-sm text-muted-foreground">
              Zobacz wszystkie wersje obok siebie
            </p>
          </div>
          <Link href={`/places/compare/${placeId}`}>
            <Button variant="outline" size="sm" className="shadow-sm hover:shadow-md transition-shadow">
              Porównaj
            </Button>
          </Link>
        </div>
      </motion.section>
    </main>
  );
}
