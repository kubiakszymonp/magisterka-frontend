"use client";

import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { Place } from "@/lib/types";

interface PlaceCardProps {
    place: Place;
    index?: number;
}

export function PlaceCard({ place, index = 0 }: PlaceCardProps) {
    return (
        <Link href={`/places/${place.id}`} className="block group">
            <motion.article
                className="border border-border bg-card rounded-md overflow-hidden shadow-sm transition-all duration-300 hover:shadow-md hover:border-foreground/20"
                whileHover={{ y: -2 }}
                transition={{ duration: 0.2 }}
            >
                <div className="relative h-60 w-full overflow-hidden bg-muted">
                    <Image
                        src={place.thumbnail}
                        alt={place.name}
                        fill
                        className="object-cover"
                    />
                </div>
                <div className="p-4">
                    <h3 className="font-medium text-foreground mb-1 group-hover:text-foreground/80 transition-colors">
                        {place.name}
                    </h3>
                    <p className="text-sm text-muted-foreground line-clamp-2">
                        {place.description}
                    </p>
                </div>
            </motion.article>
        </Link>
    );
}
