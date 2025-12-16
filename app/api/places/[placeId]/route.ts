import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export const dynamic = "force-dynamic";

export async function GET(
  request: Request,
  { params }: { params: Promise<{ placeId: string }> }
) {
  const { placeId } = await params;
  const filePath = path.join(process.cwd(), "data", "places.json");
  const fileContents = fs.readFileSync(filePath, "utf8");
  const places = JSON.parse(fileContents);
  const place = places.find((p: { id: string }) => p.id === placeId);

  if (!place) {
    return NextResponse.json({ error: "Place not found" }, { status: 404 });
  }

  return NextResponse.json(place);
}







