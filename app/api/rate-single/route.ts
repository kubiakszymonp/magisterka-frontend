import { NextResponse } from "next/server";
import { promises as fs } from "fs";
import path from "path";

const RATINGS_FILE = path.join(process.cwd(), "data/ratings/single.json");

export async function POST(request: Request) {
  try {
    const body = await request.json();

    // Create rating object
    const rating = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      placeId: body.placeId,
      articleStyle: body.articleStyle,
      clarity: parseInt(body.clarity) || 0,
      styleMatch: parseInt(body.styleMatch) || 0,
      structure: parseInt(body.structure) || 0,
      usefulness: parseInt(body.usefulness) || 0,
      length: body.length || "",
      enjoyment: parseInt(body.enjoyment) || 0,
      comment: body.comment || "",
    };

    // Read existing ratings
    let ratings = [];
    try {
      const data = await fs.readFile(RATINGS_FILE, "utf-8");
      ratings = JSON.parse(data);
    } catch {
      // File doesn't exist or is empty, start with empty array
      ratings = [];
    }

    // Add new rating
    ratings.push(rating);

    // Write back to file
    await fs.writeFile(RATINGS_FILE, JSON.stringify(ratings, null, 2), "utf-8");

    return NextResponse.json({ success: true, id: rating.id });
  } catch (error) {
    console.error("Error saving rating:", error);
    return NextResponse.json(
      { success: false, error: "Failed to save rating" },
      { status: 500 }
    );
  }
}

export async function GET() {
  try {
    const data = await fs.readFile(RATINGS_FILE, "utf-8");
    const ratings = JSON.parse(data);
    return NextResponse.json(ratings);
  } catch {
    return NextResponse.json([]);
  }
}





