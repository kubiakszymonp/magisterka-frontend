"use client";

import { useState, useRef, useMemo, useEffect } from "react";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { TextToSpeech, TextToSpeechRef, getSentenceBoundaries } from "@/components/TextToSpeech";
import { useVoice } from "@/lib/voice-context";
import { Article } from "@/lib/types";

interface ArticleTabsProps {
  articles: {
    adult_full: Article | null;
    adult_short: Article | null;
    child_full: Article | null;
  };
}

export function ArticleTabs({ articles }: ArticleTabsProps) {
  const [activeTab, setActiveTab] = useState<string>("adult_full");
  const [currentSentenceIndex, setCurrentSentenceIndex] = useState<number | null>(null);
  const { stopAllSpeech } = useVoice();
  const textToSpeechRef = useRef<TextToSpeechRef>(null);

  const tabs = [
    { key: "adult_full", label: "Dorośli pełny", article: articles.adult_full },
    { key: "adult_short", label: "Dorośli skrót", article: articles.adult_short },
    { key: "child_full", label: "Dzieci pełny", article: articles.child_full },
  ];

  const activeArticle = tabs.find(t => t.key === activeTab)?.article || null;

  // Stop speech and reset when switching tabs
  const handleTabChange = (newTab: string) => {
    stopAllSpeech();
    setCurrentSentenceIndex(null);
    setActiveTab(newTab);
  };

  // Precompute sentence boundaries for active article
  const sentenceBoundaries = useMemo(() => {
    if (!activeArticle) return [];
    return getSentenceBoundaries(activeArticle.content);
  }, [activeArticle]);

  const handleSentenceClick = (sentenceIndex: number) => {
    textToSpeechRef.current?.playFromSentence(sentenceIndex);
  };

  const renderHighlightedText = (
    content: string,
    boundaries: { start: number; end: number; text: string }[],
    currentIndex: number | null
  ) => {
    let lastEnd = 0;
    const elements: React.ReactNode[] = [];

    boundaries.forEach((boundary, index) => {
      if (boundary.start > lastEnd) {
        elements.push(
          <span key={`gap-${index}`}>
            {content.slice(lastEnd, boundary.start)}
          </span>
        );
      }

      const isHighlighted = currentIndex === index;
      elements.push(
        <span
          key={`sentence-${index}`}
          onClick={() => handleSentenceClick(index)}
          className={`cursor-pointer rounded px-1 transition-all duration-200 ${
            isHighlighted 
              ? "bg-primary/15 text-foreground border-b-2 border-primary/40" 
              : "hover:bg-muted/50"
          }`}
        >
          {boundary.text}
        </span>
      );

      lastEnd = boundary.end;
    });

    if (lastEnd < content.length) {
      elements.push(<span key="end">{content.slice(lastEnd)}</span>);
    }

    return elements;
  };

  return (
    <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
      <TabsList className="w-full justify-start bg-transparent border-b border-border rounded-none p-0 h-auto">
        {tabs.map((tab) => (
          <TabsTrigger 
            key={tab.key} 
            value={tab.key} 
            className="text-sm rounded-none border-b-2 border-transparent data-[state=active]:border-foreground data-[state=active]:bg-transparent data-[state=active]:shadow-none px-4 py-2"
          >
            {tab.label}
          </TabsTrigger>
        ))}
      </TabsList>

      {/* Render only active tab content */}
      <div className="mt-6">
        {activeArticle ? (
          <div className="space-y-4">
            <h3 className="font-medium">{activeArticle.title}</h3>
            <TextToSpeech 
              key={activeTab} // Force remount on tab change
              ref={textToSpeechRef}
              text={activeArticle.content} 
              title={activeArticle.title}
              onSentenceChange={setCurrentSentenceIndex}
            />
            <div className="text-sm text-muted-foreground leading-relaxed select-none whitespace-pre-wrap">
              {renderHighlightedText(
                activeArticle.content,
                sentenceBoundaries,
                currentSentenceIndex
              )}
            </div>
          </div>
        ) : (
          <p className="text-muted-foreground text-sm py-8">
            Artykuł niedostępny
          </p>
        )}
      </div>
    </Tabs>
  );
}
