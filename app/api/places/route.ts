import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export const dynamic = "force-dynamic";

export async function GET() {
  const filePath = path.join(process.cwd(), "data", "places.json");
  const fileContents = fs.readFileSync(filePath, "utf8");
  const places = JSON.parse(fileContents);
  return NextResponse.json(places);
}

