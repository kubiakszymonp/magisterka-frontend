"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown } from "lucide-react";

export function StudyInfoCard() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="border border-border bg-muted/30 rounded-md overflow-hidden shadow-sm transition-all duration-200 hover:shadow-md hover:bg-muted/40">
      <div className="p-6">
        <h2 className="text-sm font-medium uppercase tracking-wider text-muted-foreground mb-4">
          O badaniu
        </h2>
        <div className="space-y-3 text-sm text-muted-foreground leading-relaxed">
          <p>
            W ramach tego badania będziesz czytać różne wersje przewodników turystycznych 
            dotyczących tego samego miejsca.
          </p>
          <div className="grid grid-cols-1 gap-2 py-2">
            <div className="flex items-center gap-3">
              <span className="w-2 h-2 bg-foreground/80 rounded-full"></span>
              <span><strong className="text-foreground">Dorośli – pełny</strong> — szczegółowy tekst</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="w-2 h-2 bg-foreground/60 rounded-full"></span>
              <span><strong className="text-foreground">Dorośli – skrót</strong> — zwięzła wersja</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="w-2 h-2 bg-foreground/40 rounded-full"></span>
              <span><strong className="text-foreground">Dzieci – pełny</strong> — dla młodszych czytelników</span>
            </div>
          </div>
          <p>
            Po przeczytaniu możesz ocenić każdą wersję i porównać je między sobą.
          </p>
        </div>
      </div>

      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-6 py-3 border-t border-border bg-muted/20 hover:bg-muted/30 transition-colors flex items-center justify-between gap-2 text-sm text-muted-foreground"
      >
        <span>Więcej informacji</span>
        <motion.div
          animate={{ rotate: isExpanded ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <ChevronDown className="h-4 w-4" />
        </motion.div>
      </button>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-6 pb-6 pt-4 border-t border-border space-y-4 text-sm text-muted-foreground leading-relaxed">
              <div>
                <h3 className="font-medium text-foreground mb-2">Cel badania</h3>
                <p>
                  Celem tego badania jest ocena efektywności różnych stylów pisania przewodników turystycznych. 
                  Chcemy zrozumieć, które podejścia są najbardziej skuteczne w przekazywaniu informacji turystycznych 
                  różnym grupom odbiorców.
                </p>
              </div>
              
              <div>
                <h3 className="font-medium text-foreground mb-2">Co będziemy mierzyć</h3>
                <ul className="space-y-2 list-disc list-inside ml-2">
                  <li><strong className="text-foreground">Zrozumiałość</strong> — jak łatwo jest zrozumieć przekazywane informacje</li>
                  <li><strong className="text-foreground">Dopasowanie stylu</strong> — czy styl pisania odpowiada grupie docelowej</li>
                  <li><strong className="text-foreground">Struktura tekstu</strong> — przejrzystość i organizacja treści</li>
                  <li><strong className="text-foreground">Przydatność turystyczna</strong> — praktyczna wartość informacji dla turysty</li>
                  <li><strong className="text-foreground">Długość tekstu</strong> — czy objętość jest odpowiednia</li>
                  <li><strong className="text-foreground">Przyjemność czytania</strong> — subiektywne odczucia podczas lektury</li>
                </ul>
              </div>

              <div>
                <h3 className="font-medium text-foreground mb-2">Jak to działa</h3>
                <p>
                  Wybierz miejsce, przeczytaj wszystkie trzy wersje przewodnika, ocen każdą z nich osobno, 
                  a następnie porównaj je w ankiecie porównawczej. Twoje opinie pomogą nam zrozumieć, 
                  które style są najbardziej skuteczne.
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
