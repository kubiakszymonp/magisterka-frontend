import { Place, Article } from "./types";

export async function getPlaces(): Promise<Place[]> {
  const res = await fetch("/api/places", { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export async function getPlace(id: string): Promise<Place | undefined> {
  const res = await fetch(`/api/places/${id}`, { cache: "no-store" });
  if (!res.ok) return undefined;
  return res.json();
}

export async function getArticle(
  placeId: string,
  style: string
): Promise<Article | null> {
  const res = await fetch(`/api/articles/${placeId}/${style}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

export async function getAllArticlesForPlace(
  placeId: string
): Promise<{ adult_full: Article | null; adult_short: Article | null; child_short: Article | null }> {
  const [adult_full, adult_short, child_short] = await Promise.all([
    getArticle(placeId, "adult_full"),
    getArticle(placeId, "adult_short"),
    getArticle(placeId, "child_short"),
  ]);

  return { adult_full, adult_short, child_short };
}

