"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Article } from "@/lib/types";

interface ArticleCardProps {
  article: Article;
  label: string;
  icon: string;
  index?: number;
}

export function ArticleCard({ article, label }: ArticleCardProps) {
  return (
    <Link href={`/places/${article.placeId}/${article.style}`} className="block group">
      <motion.article
        className="border border-border bg-card rounded-md overflow-hidden shadow-sm transition-all duration-300 hover:shadow-md hover:border-foreground/20 h-full"
        whileHover={{ y: -2 }}
        transition={{ duration: 0.2 }}
      >
        <div className="p-4">
          <h3 className="font-medium text-sm mb-1 group-hover:text-foreground/80 transition-colors">
            {label}
          </h3>
          <p className="text-xs text-muted-foreground mb-3">
            Kliknij, aby przeczytać i ocenić
          </p>
          <div className="text-xs text-muted-foreground/60">
            {article.title}
          </div>
        </div>
      </motion.article>
    </Link>
  );
}
