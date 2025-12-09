import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export const dynamic = "force-dynamic";

export async function GET() {
  const filePath = path.join(process.cwd(), "data", "places.json");
  console.log(filePath);
  const fileContents = fs.readFileSync(filePath, "utf8");
  console.log(fileContents);
  const places = JSON.parse(fileContents);
  console.log(places);
  return NextResponse.json(places);
}





