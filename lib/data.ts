import { Place, Article } from "./types";
import placesData from "@/data/places.json";

export function getPlaces(): Place[] {
  return placesData as Place[];
}

export function getPlace(id: string): Place | undefined {
  return placesData.find((place) => place.id === id) as Place | undefined;
}

export async function getArticle(
  placeId: string,
  style: string
): Promise<Article | null> {
  try {
    const article = await import(`@/data/articles/${placeId}_${style}.json`);
    return article.default as Article;
  } catch {
    return null;
  }
}

export async function getAllArticlesForPlace(
  placeId: string
): Promise<{ adult_full: Article | null; adult_short: Article | null; child_full: Article | null }> {
  const [adult_full, adult_short, child_full] = await Promise.all([
    getArticle(placeId, "adult_full"),
    getArticle(placeId, "adult_short"),
    getArticle(placeId, "child_full"),
  ]);

  return { adult_full, adult_short, child_full };
}

