"use client";

import { createContext, useContext, useState, useEffect, ReactNode, useRef, useCallback } from "react";

interface VoiceSettings {
  rate: number;
  pitch: number;
  volume: number;
  pauseDuration: number; // in milliseconds
}

interface VoiceContextType {
  selectedVoice: string;
  setSelectedVoice: (voice: string) => void;
  voices: SpeechSynthesisVoice[];
  settings: VoiceSettings;
  setSettings: (settings: Partial<VoiceSettings>) => void;
  stopAllSpeech: () => void;
}

const VoiceContext = createContext<VoiceContextType | undefined>(undefined);

const defaultSettings: VoiceSettings = {
  rate: 1.0,
  pitch: 1.0,
  volume: 1.0,
  pauseDuration: 300, // 300ms default pause between sentences
};

export function VoiceProvider({ children }: { children: ReactNode }) {
  const [selectedVoice, setSelectedVoiceState] = useState<string>("");
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);
  const [settings, setSettingsState] = useState<VoiceSettings>(defaultSettings);

  const stopAllSpeech = useCallback(() => {
    if (typeof window !== "undefined" && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  }, []);

  useEffect(() => {
    // Load settings from localStorage
    const savedSettings = localStorage.getItem("voiceSettings");
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings);
        setSettingsState({ ...defaultSettings, ...parsed });
      } catch (e) {
        // Ignore parse errors
      }
    }
  }, []);

  useEffect(() => {
    const loadVoices = () => {
      if (typeof window === "undefined" || !window.speechSynthesis) return;
      
      const availableVoices = window.speechSynthesis.getVoices();
      
      // Prioritize Polish voices, then English
      const polishVoices = availableVoices.filter((voice) => voice.lang.startsWith("pl"));
      const englishVoices = availableVoices.filter((voice) => voice.lang.startsWith("en"));
      const filteredVoices = [...polishVoices, ...englishVoices];
      
      setVoices(filteredVoices);
      
      // Load from localStorage or auto-select Polish voice
      const savedVoice = localStorage.getItem("selectedVoice");
      if (savedVoice && filteredVoices.find(v => v.voiceURI === savedVoice)) {
        setSelectedVoiceState(savedVoice);
      } else if (polishVoices.length > 0) {
        // Prefer Polish male voice
        const maleVoice = polishVoices.find(
          (v) => v.name.toLowerCase().includes("male") || 
                 v.name.toLowerCase().includes("męski") ||
                 v.name.toLowerCase().includes("adam") ||
                 v.name.toLowerCase().includes("mężczyzna") ||
                 v.name.toLowerCase().includes("jacek")
        );
        const voiceToSet = maleVoice || polishVoices[0];
        setSelectedVoiceState(voiceToSet.voiceURI);
        localStorage.setItem("selectedVoice", voiceToSet.voiceURI);
      } else if (filteredVoices.length > 0) {
        setSelectedVoiceState(filteredVoices[0].voiceURI);
        localStorage.setItem("selectedVoice", filteredVoices[0].voiceURI);
      }
    };

    loadVoices();
    if (typeof window !== "undefined" && window.speechSynthesis) {
      window.speechSynthesis.onvoiceschanged = loadVoices;
    }
  }, []);

  const setSelectedVoice = (voice: string) => {
    setSelectedVoiceState(voice);
    localStorage.setItem("selectedVoice", voice);
  };

  const setSettings = (newSettings: Partial<VoiceSettings>) => {
    const updated = { ...settings, ...newSettings };
    setSettingsState(updated);
    localStorage.setItem("voiceSettings", JSON.stringify(updated));
  };

  return (
    <VoiceContext.Provider value={{ selectedVoice, setSelectedVoice, voices, settings, setSettings, stopAllSpeech }}>
      {children}
    </VoiceContext.Provider>
  );
}

export function useVoice() {
  const context = useContext(VoiceContext);
  if (context === undefined) {
    throw new Error("useVoice must be used within a VoiceProvider");
  }
  return context;
}
