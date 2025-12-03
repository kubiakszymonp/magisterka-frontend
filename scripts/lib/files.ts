import * as fs from "fs";
import * as path from "path";
import type { Place, SourceArticle, GeneratedArticle, GenerationLog } from "./types";

// === Paths ===

const DATA_DIR = path.join(process.cwd(), "data");
export const PLACES_FILE = path.join(DATA_DIR, "places.json");
export const SOURCE_ARTICLES_DIR = path.join(DATA_DIR, "source-articles");
export const OUTPUT_DIR = path.join(DATA_DIR, "articles");
export const LOGS_DIR = path.join(DATA_DIR, "generation-logs");

// === Load Functions ===

export function loadPlaces(): Map<string, Place> {
  const content = fs.readFileSync(PLACES_FILE, "utf-8");
  const places: Place[] = JSON.parse(content);
  return new Map(places.map((p) => [p.id, p]));
}

export function loadSourceArticles(placeId: string): SourceArticle[] {
  const filePath = path.join(SOURCE_ARTICLES_DIR, `${placeId}.json`);

  if (!fs.existsSync(filePath)) {
    return [];
  }

  const content = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(content);
}

export function getSourceArticleIds(): string[] {
  const files = fs.readdirSync(SOURCE_ARTICLES_DIR);
  return files
    .filter((file) => file.endsWith(".json"))
    .map((file) => file.replace(".json", ""));
}

// === Save Functions ===

function ensureDir(dirPath: string): void {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

export function saveArticle(article: GeneratedArticle): void {
  const placeDir = path.join(OUTPUT_DIR, article.placeId);
  ensureDir(placeDir);

  const filePath = path.join(placeDir, `${article.style}.json`);
  fs.writeFileSync(filePath, JSON.stringify(article, null, 2), "utf-8");
}

export function saveGenerationLog(log: GenerationLog): void {
  const placeDir = path.join(LOGS_DIR, log.place_id);
  ensureDir(placeDir);

  const filePath = path.join(placeDir, `${log.style}.json`);
  fs.writeFileSync(filePath, JSON.stringify(log, null, 2), "utf-8");
}

