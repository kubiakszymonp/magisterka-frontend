import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export const dynamic = "force-dynamic";

export async function GET(
  request: Request,
  { params }: { params: Promise<{ placeId: string; style: string }> }
) {
  const { placeId, style } = await params;

  try {
    const filePath = path.join(
      process.cwd(),
      "data",
      "articles",
      `${placeId}_${style}.json`
    );
    const fileContents = fs.readFileSync(filePath, "utf8");
    const article = JSON.parse(fileContents);
    return NextResponse.json(article);
  } catch {
    return NextResponse.json({ error: "Article not found" }, { status: 404 });
  }
}

