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
const BATCH_SIZE = parseInt(process.argv.find((a) => a.startsWith("--batch="))?.split("=")[1] ?? "5", 10);

// === Utils ===

function chunk<T>(array: T[], size: number): T[][] {
  const chunks: T[][] = [];
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size));
  }
  return chunks;
}

// === Main ===

async function processPlace(placeId: string, placeName: string, sourceArticles: SourceArticle[]): Promise<number> {
  const tag = `[${placeName}]`;
  console.log(`${tag} → Generowanie ${VARIANTS.length} wariantów...`);

  const results = await Promise.all(
    VARIANTS.map(async (variant) => {
      const ctx: ChainContext = {
        placeId,
        placeName,
        sourceArticles,
        variant,
      };

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

      console.log(`${tag} ✓ ${variant.style}: ${log.total_tokens} tokens, ${log.total_duration_ms}ms`);

      return log;
    })
  );

  console.log(`${tag} ✅ Zakończono (${results.length} wariantów)`);
  return results.length;
}

async function main(): Promise<void> {
  console.log("🚀 Rozpoczynam przetwarzanie artykułów...\n");

  const places = loadPlaces();
  console.log(`📍 Załadowano ${places.size} miejsc`);

  const sourceIds = SINGLE_PLACE ? [SINGLE_PLACE] : getSourceArticleIds();
  console.log(`📄 Do przetworzenia: ${sourceIds.length} miejsc`);
  console.log(`⚡ Rozmiar batcha: ${BATCH_SIZE} miejsc równolegle\n`);

  let processedCount = 0;
  let skippedCount = 0;
  let articlesCount = 0;

  // Przygotuj dane miejsc do przetworzenia
  const placesToProcess: { placeId: string; placeName: string; sources: SourceArticle[] }[] = [];

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

    placesToProcess.push({ placeId, placeName: place.name, sources });
  }

  // Przetwarzaj w batchach
  const batches = chunk(placesToProcess, BATCH_SIZE);

  for (let i = 0; i < batches.length; i++) {
    const batch = batches[i];
    const placeNames = batch.map((p) => p.placeName).join(", ");
    console.log(`\n📦 Batch ${i + 1}/${batches.length}: ${placeNames}`);

    const results = await Promise.all(
      batch.map(async ({ placeId, placeName, sources }) => {
        const count = await processPlace(placeId, placeName, sources);
        return count;
      })
    );

    for (const count of results) {
      articlesCount += count;
      processedCount++;
    }
  }

  console.log(`\n📊 Podsumowanie:`);
  console.log(`   Przetworzono: ${processedCount} miejsc`);
  console.log(`   Pominięto: ${skippedCount} miejsc`);
  console.log(`   Wygenerowano: ${articlesCount} artykułów`);
  console.log(`\n✨ Gotowe!`);
}

main().catch(console.error);
