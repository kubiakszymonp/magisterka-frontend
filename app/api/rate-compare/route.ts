import { NextResponse } from "next/server";
import { promises as fs } from "fs";
import path from "path";

const RATINGS_FILE = path.join(process.cwd(), "data/ratings/compare.json");

export async function POST(request: Request) {
  try {
    const body = await request.json();

    // Create rating object
    const rating = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      placeId: body.placeId,
      bestOverall: body.bestOverall || "",
      easiestToUnderstand: body.easiestToUnderstand || "",
      bestForChildren: body.bestForChildren || "",
      bestForQuickLook: body.bestForQuickLook || "",
      bestForPlanning: body.bestForPlanning || "",
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
    console.error("Error saving comparison:", error);
    return NextResponse.json(
      { success: false, error: "Failed to save comparison" },
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





