#!/usr/bin/env tsx

import {
  loadPlaces,
  loadSourceArticles,
  getSourceArticleIds,
  saveArticle,
  saveGenerationLog,
} from "./lib/files";
import { VARIANTS, type GeneratedArticle, type ChainContext, type SourceArticle } from "./lib/types";
import { runChain } from "./lib/chain";

// === Config ===

const SINGLE_PLACE = process.argv.find((a) => a.startsWith("--place="))?.split("=")[1];

// === Main ===

async function processPlace(placeId: string, placeName: string, sourceArticles: SourceArticle[]): Promise<number> {
  let generated = 0;

  for (const variant of VARIANTS) {
    const ctx: ChainContext = {
      placeId,
      placeName,
      sourceArticles,
      variant,
    };

    console.log(`  → ${variant.style}...`);

    const { result, log } = await runChain(ctx);

    const article: GeneratedArticle = {
      placeId,
      style: variant.style,
      ageTarget: variant.ageTarget,
      volume: variant.volume,
      title: result.title.trim(),
      content: result.markdown,
    };

    saveArticle(article);
    saveGenerationLog(log);

    console.log(`    ✓ ${log.total_tokens} tokens, ${log.total_duration_ms}ms`);
    generated++;
  }

  return generated;
}

async function main(): Promise<void> {
  console.log("🚀 Rozpoczynam przetwarzanie artykułów...\n");

  const places = loadPlaces();
  console.log(`📍 Załadowano ${places.size} miejsc`);

  const sourceIds = SINGLE_PLACE ? [SINGLE_PLACE] : getSourceArticleIds();
  console.log(`📄 Do przetworzenia: ${sourceIds.length} miejsc\n`);

  let processedCount = 0;
  let skippedCount = 0;
  let articlesCount = 0;

  for (const placeId of sourceIds) {
    const place = places.get(placeId);

    if (!place) {
      console.warn(`⚠️  Brak w places.json: ${placeId}`);
      skippedCount++;
      continue;
    }

    const sources = loadSourceArticles(placeId);

    if (sources.length === 0) {
      console.warn(`⚠️  Brak źródeł: ${placeId}`);
      skippedCount++;
      continue;
    }

    console.log(`📝 ${place.name}`);

    const count = await processPlace(placeId, place.name, sources);

    articlesCount += count;
    processedCount++;
  }

  console.log(`\n📊 Podsumowanie:`);
  console.log(`   Przetworzono: ${processedCount} miejsc`);
  console.log(`   Pominięto: ${skippedCount} miejsc`);
  console.log(`   Wygenerowano: ${articlesCount} artykułów`);
  console.log(`\n✨ Gotowe!`);
}

main().catch(console.error);
