import { useState, useEffect, useRef, useCallback } from "react";
import { useVoice } from "@/lib/voice-context";

// Split text into sentences/phrases by punctuation
const splitIntoSentences = (text: string): string[] => {
  const sentences = text.split(/(?<=[.!?;:])\s+/).filter(s => s.trim().length > 0);
  return sentences;
};

export function useTextToSpeech(text: string, onSentenceChange?: (sentenceIndex: number | null) => void) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const { selectedVoice, voices, settings, stopAllSpeech } = useVoice();
  const sentencesRef = useRef<string[]>([]);
  const currentIndexRef = useRef<number>(0);
  const isStoppedRef = useRef<boolean>(false);
  const isPausedRef = useRef<boolean>(false);
  const settingsRef = useRef(settings);
  const selectedVoiceRef = useRef(selectedVoice);
  const voicesRef = useRef(voices);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const isPlayingRef = useRef(false);
  const lastSettingsChangeRef = useRef<number>(0);

  // Keep refs in sync
  useEffect(() => {
    settingsRef.current = settings;
    selectedVoiceRef.current = selectedVoice;
    voicesRef.current = voices;
  }, [settings, selectedVoice, voices]);

  // Split text into sentences
  useEffect(() => {
    sentencesRef.current = splitIntoSentences(text);
  }, [text]);

  const speakSentence = useCallback((sentenceIndex: number) => {
    if (typeof window === "undefined" || !window.speechSynthesis) return;
    if (isStoppedRef.current || isPausedRef.current) return;
    if (sentenceIndex >= sentencesRef.current.length) {
      setIsPlaying(false);
      isPlayingRef.current = false;
      setIsPaused(false);
      onSentenceChange?.(null);
      return;
    }

    const sentence = sentencesRef.current[sentenceIndex];
    const utterance = new SpeechSynthesisUtterance(sentence);

    // Use refs to get latest values
    const currentSettings = settingsRef.current;
    const currentVoice = selectedVoiceRef.current;
    const currentVoices = voicesRef.current;

    // Set voice using ref
    if (currentVoice && currentVoices.length > 0) {
      const voice = currentVoices.find((v) => v.voiceURI === currentVoice);
      if (voice) {
        utterance.voice = voice;
        utterance.lang = voice.lang;
      }
    } else {
      utterance.lang = "pl-PL";
    }

    // Apply current settings
    utterance.rate = currentSettings.rate;
    utterance.pitch = currentSettings.pitch;
    utterance.volume = currentSettings.volume;

    utterance.onstart = () => {
      currentIndexRef.current = sentenceIndex;
      onSentenceChange?.(sentenceIndex);
    };

    utterance.onend = () => {
      if (!isStoppedRef.current && !isPausedRef.current) {
        // Use current pause duration from settings
        const pauseDuration = settingsRef.current.pauseDuration;
        if (timeoutRef.current) {
          clearTimeout(timeoutRef.current);
        }
        timeoutRef.current = setTimeout(() => {
          if (!isStoppedRef.current && !isPausedRef.current) {
            speakSentence(sentenceIndex + 1);
          }
        }, pauseDuration);
      }
    };

    utterance.onerror = (e) => {
      if (e.error !== "interrupted" && e.error !== "canceled") {
        console.error("Speech error:", e.error);
        if (!isStoppedRef.current && !isPausedRef.current) {
          speakSentence(sentenceIndex + 1);
        }
      }
    };

    window.speechSynthesis.speak(utterance);
  }, [onSentenceChange]);

  // React to settings changes - restart current sentence if playing
  useEffect(() => {
    // Only restart if actually playing and settings changed (not on initial play)
    const now = Date.now();
    if (isPlayingRef.current && now - lastSettingsChangeRef.current > 100) {
      lastSettingsChangeRef.current = now;
      
      if (typeof window !== "undefined" && window.speechSynthesis) {
        const currentIndex = currentIndexRef.current;
        
        // Cancel current utterance
        window.speechSynthesis.cancel();
        if (timeoutRef.current) {
          clearTimeout(timeoutRef.current);
          timeoutRef.current = null;
        }
        
        // Small delay to ensure cancellation, then restart with new settings
        const timeoutId = setTimeout(() => {
          if (isPlayingRef.current && !isPausedRef.current) {
            speakSentence(currentIndex);
          }
        }, 50);

        return () => clearTimeout(timeoutId);
      }
    }
  }, [settings.rate, settings.pitch, settings.volume, settings.pauseDuration, selectedVoice, speakSentence]);

  const playFromSentence = useCallback((startFromSentence: number = 0) => {
    if (typeof window === "undefined" || !window.speechSynthesis) return;

    // Stop all other speech instances
    stopAllSpeech();
    
    // Clear any pending timeouts
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    
    isStoppedRef.current = false;
    isPausedRef.current = false;
    currentIndexRef.current = startFromSentence;
    lastSettingsChangeRef.current = Date.now(); // Prevent immediate restart from settings effect

    setIsPlaying(true);
    isPlayingRef.current = true;
    setIsPaused(false);

    // Small delay to ensure state is set
    setTimeout(() => {
      speakSentence(startFromSentence);
    }, 10);
  }, [speakSentence, stopAllSpeech]);

  const play = useCallback(() => {
    if (isPaused) {
      isPausedRef.current = false;
      setIsPaused(false);
      setIsPlaying(true);
      isPlayingRef.current = true;
      speakSentence(currentIndexRef.current);
      return;
    }
    playFromSentence(0);
  }, [isPaused, playFromSentence, speakSentence]);

  const pause = useCallback(() => {
    isPausedRef.current = true;
    if (typeof window !== "undefined" && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    setIsPlaying(false);
    isPlayingRef.current = false;
    setIsPaused(true);
  }, []);

  const stop = useCallback(() => {
    isStoppedRef.current = true;
    isPausedRef.current = false;
    if (typeof window !== "undefined" && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    setIsPlaying(false);
    isPlayingRef.current = false;
    setIsPaused(false);
    onSentenceChange?.(null);
  }, [onSentenceChange]);

  // Cleanup
  useEffect(() => {
    return () => {
      isStoppedRef.current = true;
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      if (typeof window !== "undefined" && window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  return {
    isPlaying,
    isPaused,
    play,
    pause,
    stop,
    playFromSentence,
  };
}
