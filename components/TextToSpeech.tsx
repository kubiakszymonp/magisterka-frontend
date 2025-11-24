"use client";

import { useImperativeHandle, forwardRef } from "react";
import { Play, Pause, Square } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useTextToSpeech } from "@/hooks/useTextToSpeech";

interface TextToSpeechProps {
  text: string;
  title?: string;
  onSentenceChange?: (sentenceIndex: number | null) => void;
}

export interface TextToSpeechRef {
  playFromSentence: (sentenceIndex: number) => void;
}

export const TextToSpeech = forwardRef<TextToSpeechRef, TextToSpeechProps>(
  ({ text, title, onSentenceChange }, ref) => {
    const { isPlaying, isPaused, play, pause, stop, playFromSentence } = useTextToSpeech(
      text,
      onSentenceChange
    );

    useImperativeHandle(ref, () => ({
      playFromSentence,
    }));

    if (typeof window === "undefined" || !window.speechSynthesis) {
      return null;
    }

    return (
      <div className="flex items-center gap-2 p-3 bg-muted/50 rounded-md border border-border">
        <div className="flex-1">
          <p className="text-xs font-medium text-foreground mb-1">
            {title || "Odsłuchaj tekst"}
          </p>
          <p className="text-xs text-muted-foreground">
            {isPlaying ? "Odtwarzanie..." : isPaused ? "Wstrzymano — kliknij ▶ aby kontynuować" : "Kliknij zdanie lub ▶, aby rozpocząć"}
          </p>
        </div>
        <div className="flex items-center gap-1">
          {(!isPlaying || isPaused) && (
            <Button
              onClick={play}
              size="sm"
              variant="outline"
              className="h-8 w-8 p-0"
              title={isPaused ? "Kontynuuj" : "Odtwórz od początku"}
            >
              <Play className="h-3 w-3" />
            </Button>
          )}
          {isPlaying && !isPaused && (
            <Button
              onClick={pause}
              size="sm"
              variant="outline"
              className="h-8 w-8 p-0"
              title="Pauza"
            >
              <Pause className="h-3 w-3" />
            </Button>
          )}
          {(isPlaying || isPaused) && (
            <Button
              onClick={stop}
              size="sm"
              variant="outline"
              className="h-8 w-8 p-0"
              title="Zatrzymaj"
            >
              <Square className="h-3 w-3" />
            </Button>
          )}
        </div>
      </div>
    );
  }
);

TextToSpeech.displayName = "TextToSpeech";

// Helper to split text and get sentence boundaries
export const splitIntoSentences = (text: string): string[] => {
  return text.split(/(?<=[.!?;:])\s+/).filter(s => s.trim().length > 0);
};

export const getSentenceBoundaries = (text: string): { start: number; end: number; text: string }[] => {
  const sentences = splitIntoSentences(text);
  const boundaries: { start: number; end: number; text: string }[] = [];
  let currentPos = 0;

  sentences.forEach((sentence) => {
    const start = text.indexOf(sentence, currentPos);
    if (start !== -1) {
      boundaries.push({
        start,
        end: start + sentence.length,
        text: sentence,
      });
      currentPos = start + sentence.length;
    }
  });

  return boundaries;
};
