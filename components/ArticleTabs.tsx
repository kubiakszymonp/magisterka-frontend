"use client";

import { useState, useRef } from "react";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { TextToSpeech, TextToSpeechRef } from "@/components/TextToSpeech";
import { useVoice } from "@/lib/voice-context";
import { Article } from "@/lib/types";
import { HighlightedHtml, stripMarkdown } from "@/utils/highlightedHtml";

interface ArticleTabsProps {
  articles: {
    adult_full: Article | null;
    adult_short: Article | null;
    child_short: Article | null;
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
    { key: "child_short", label: "Dzieci skrót", article: articles.child_short },
  ];

  const activeArticle = tabs.find(t => t.key === activeTab)?.article || null;

  // Stop speech and reset when switching tabs
  const handleTabChange = (newTab: string) => {
    stopAllSpeech();
    setCurrentSentenceIndex(null);
    setActiveTab(newTab);
  };

  const handleSentenceClick = (sentenceIndex: number) => {
    textToSpeechRef.current?.playFromSentence(sentenceIndex);
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
            <div className="bg-card border border-border rounded-md p-6 shadow-sm">
              <div className="mb-4">
                <TextToSpeech 
                  key={activeTab} // Force remount on tab change
                  ref={textToSpeechRef}
                  text={stripMarkdown(activeArticle.content)} 
                  title={activeArticle.title}
                  onSentenceChange={setCurrentSentenceIndex}
                />
              </div>
              <div className="text-sm leading-relaxed text-muted-foreground select-none prose-headings:text-foreground">
                <HighlightedHtml
                  markdown={activeArticle.content}
                  currentSentenceIndex={currentSentenceIndex}
                  onSentenceClick={handleSentenceClick}
                />
              </div>
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
