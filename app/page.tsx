"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getPlaces } from "@/lib/data";
import { PlaceCard } from "@/components/PlaceCard";
import { StudyInfoCard } from "@/components/StudyInfoCard";
import { Place } from "@/lib/types";

export default function HomePage() {
  const [places, setPlaces] = useState<Place[]>([]);

  useEffect(() => {
    getPlaces().then(setPlaces);
  }, []);

  return (
    <main className="container mx-auto px-4 py-16 max-w-4xl">
      {/* Header */}
      <header className="mb-16">
        <h1 className="text-3xl font-medium tracking-tight mb-3">
          Badanie przewodników turystycznych
        </h1>
        <p className="text-muted-foreground">
          Ocena różnych stylów pisania przewodników turystycznych.
        </p>
      </header>

      {/* Study description */}
      <section className="mb-16">
        <StudyInfoCard />
      </section>

      {/* Places grid */}
      <section>
        <h2 className="text-sm font-medium uppercase tracking-wider text-muted-foreground mb-6">
          Wybierz miejsce
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {places.map((place, index) => (
            <PlaceCard key={place.id} place={place} index={index} />
          ))}
        </div>
      </section>
    </main>
  );
}
