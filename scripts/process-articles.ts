#!/usr/bin/env tsx

import * as fs from "fs";
import * as path from "path";

// Types
interface Place {
  id: string;
  name: string;
  thumbnail: string;
  description: string;
}

interface SourceArticle {
  sourceUrl: string;
  content: string;
  comment: string;
}

interface GeneratedArticle {
  placeId: string;
  style: string;
  ageTarget: "adult" | "child";
  volume: "full" | "short";
  title: string;
  content: string;
}

// Configuration
const VARIANTS = [
  { style: "adult_full", ageTarget: "adult" as const, volume: "full" as const, prefix: "[Pełny przewodnik]\n\n" },
  { style: "adult_short", ageTarget: "adult" as const, volume: "short" as const, prefix: "[Krótki przewodnik]\n\n" },
  { style: "child_short", ageTarget: "child" as const, volume: "short" as const, prefix: "[Przewodnik dla dzieci]\n\n" },
];

// Paths
const DATA_DIR = path.join(process.cwd(), "data");
const PLACES_FILE = path.join(DATA_DIR, "places.json");
const SOURCE_ARTICLES_DIR = path.join(DATA_DIR, "source-articles");
const OUTPUT_DIR = path.join(DATA_DIR, "articles");

function loadPlaces(): Map<string, Place> {
  const content = fs.readFileSync(PLACES_FILE, "utf-8");
  const places: Place[] = JSON.parse(content);
  const placesMap = new Map<string, Place>();
  
  for (const place of places) {
    placesMap.set(place.id, place);
  }
  
  return placesMap;
}

function loadSourceArticles(placeId: string): SourceArticle[] {
  const filePath = path.join(SOURCE_ARTICLES_DIR, `${placeId}.json`);
  
  if (!fs.existsSync(filePath)) {
    console.warn(`⚠️  Brak pliku źródłowego dla: ${placeId}`);
    return [];
  }
  
  const content = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(content);
}

function combineContent(sources: SourceArticle[]): string {
  return sources
    .map((source) => source.content)
    .filter((content) => content.trim().length > 0)
    .join("\n\n---\n\n");
}

function generateArticle(
  placeId: string,
  placeName: string,
  combinedContent: string,
  variant: typeof VARIANTS[number]
): GeneratedArticle {
  return {
    placeId,
    style: variant.style,
    ageTarget: variant.ageTarget,
    volume: variant.volume,
    title: placeName,
    content: variant.prefix + combinedContent,
  };
}

function ensureDir(dirPath: string): void {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

function saveArticle(article: GeneratedArticle): void {
  const placeDir = path.join(OUTPUT_DIR, article.placeId);
  ensureDir(placeDir);
  
  const filePath = path.join(placeDir, `${article.style}.json`);
  fs.writeFileSync(filePath, JSON.stringify(article, null, 2), "utf-8");
}

function getSourceArticleIds(): string[] {
  const files = fs.readdirSync(SOURCE_ARTICLES_DIR);
  return files
    .filter((file) => file.endsWith(".json"))
    .map((file) => file.replace(".json", ""));
}

function main(): void {
  console.log("🚀 Rozpoczynam przetwarzanie artykułów...\n");

  // Load places
  const places = loadPlaces();
  console.log(`📍 Załadowano ${places.size} miejsc z places.json`);

  // Get source article IDs
  const sourceIds = getSourceArticleIds();
  console.log(`📄 Znaleziono ${sourceIds.length} plików źródłowych\n`);

  let processedCount = 0;
  let skippedCount = 0;

  for (const placeId of sourceIds) {
    const place = places.get(placeId);
    
    if (!place) {
      console.warn(`⚠️  Brak miejsca w places.json dla: ${placeId}`);
      skippedCount++;
      continue;
    }

    // Load sources
    const sources = loadSourceArticles(placeId);
    
    if (sources.length === 0) {
      skippedCount++;
      continue;
    }

    // Combine content
    const combinedContent = combineContent(sources);

    // Generate all variants
    for (const variant of VARIANTS) {
      const article = generateArticle(placeId, place.name, combinedContent, variant);
      saveArticle(article);
    }

    console.log(`✅ ${place.name} (${VARIANTS.length} warianty)`);
    processedCount++;
  }

  console.log(`\n📊 Podsumowanie:`);
  console.log(`   Przetworzono: ${processedCount} miejsc`);
  console.log(`   Pominięto: ${skippedCount} miejsc`);
  console.log(`   Wygenerowano: ${processedCount * VARIANTS.length} artykułów`);
  console.log(`\n✨ Gotowe!`);
}

main();

