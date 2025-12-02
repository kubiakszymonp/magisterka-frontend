#!/usr/bin/env tsx

import {
  loadPlaces,
  loadSourceArticles,
  getSourceArticleIds,
  combineSourceContent,
  saveArticle,
} from "./lib/files";
import { VARIANTS, type GeneratedArticle, type ChainContext } from "./lib/types";
import { runChain, dryRunChain } from "./lib/openai";

// === Config ===

const DRY_RUN = process.argv.includes("--dry-run");
const SINGLE_PLACE = process.argv.find((a) => a.startsWith("--place="))?.split("=")[1];

// === Main ===

async function processPlace(placeId: string, placeName: string, sourceContent: string): Promise<number> {
  let generated = 0;

  for (const variant of VARIANTS) {
    const ctx: ChainContext = {
      placeId,
      placeName,
      sourceContent,
      variant,
    };

    if (DRY_RUN) {
      dryRunChain(ctx);
      continue;
    }

    console.log(`  → ${variant.style}...`);

    const result = await runChain(ctx);

    const article: GeneratedArticle = {
      placeId,
      style: variant.style,
      ageTarget: variant.ageTarget,
      volume: variant.volume,
      title: result.title.trim(),
      content: result.markdown,
    };

    saveArticle(article);
    generated++;
  }

  return generated;
}

async function main(): Promise<void> {
  console.log("🚀 Rozpoczynam przetwarzanie artykułów...\n");

  if (DRY_RUN) {
    console.log("⚠️  Tryb DRY RUN - bez wywołań API\n");
  }

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

    const sourceContent = combineSourceContent(sources);
    const count = await processPlace(placeId, place.name, sourceContent);

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
