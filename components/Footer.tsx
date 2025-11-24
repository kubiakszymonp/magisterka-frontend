"use client";

import { useVoice } from "@/lib/voice-context";
import { Volume2, Gauge, Music, Volume, Pause } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";

export function Footer() {
  const { selectedVoice, setSelectedVoice, voices, settings, setSettings } = useVoice();

  if (voices.length === 0) {
    return null;
  }

  return (
    <footer className="border-t border-border mt-auto py-4 px-4 bg-card/50">
      <div className="container mx-auto max-w-6xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          {/* Voice selection */}
          <div className="flex items-center gap-3 flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-shrink-0">
              <Volume2 className="h-4 w-4 text-muted-foreground" />
              <Label htmlFor="voice-select" className="text-sm text-muted-foreground whitespace-nowrap">
                Głos:
              </Label>
            </div>
            <Select value={selectedVoice} onValueChange={setSelectedVoice}>
              <SelectTrigger id="voice-select" className="h-8 w-full md:w-[250px] text-xs">
                <SelectValue placeholder="Wybierz głos" />
              </SelectTrigger>
              <SelectContent>
                {voices.map((voice) => (
                  <SelectItem key={voice.voiceURI} value={voice.voiceURI}>
                    {voice.name} {voice.lang}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Settings */}
          <div className="flex items-center gap-4 flex-wrap flex-1 justify-end">
            {/* Rate */}
            <div className="flex items-center gap-2 min-w-[120px]">
              <Gauge className="h-3.5 w-3.5 text-muted-foreground" />
              <div className="flex-1">
                <Label htmlFor="rate-slider" className="text-xs text-muted-foreground">
                  Tempo: {settings.rate.toFixed(1)}x
                </Label>
                <input
                  id="rate-slider"
                  type="range"
                  min="0.5"
                  max="2.0"
                  step="0.1"
                  value={settings.rate}
                  onChange={(e) => setSettings({ rate: parseFloat(e.target.value) })}
                  className="w-full h-1.5 bg-muted rounded-lg appearance-none cursor-pointer accent-foreground/20"
                />
              </div>
            </div>

            {/* Pitch */}
            <div className="flex items-center gap-2 min-w-[120px]">
              <Music className="h-3.5 w-3.5 text-muted-foreground" />
              <div className="flex-1">
                <Label htmlFor="pitch-slider" className="text-xs text-muted-foreground">
                  Wysokość: {settings.pitch.toFixed(1)}
                </Label>
                <input
                  id="pitch-slider"
                  type="range"
                  min="0.5"
                  max="2.0"
                  step="0.1"
                  value={settings.pitch}
                  onChange={(e) => setSettings({ pitch: parseFloat(e.target.value) })}
                  className="w-full h-1.5 bg-muted rounded-lg appearance-none cursor-pointer accent-foreground/20"
                />
              </div>
            </div>

            {/* Volume */}
            <div className="flex items-center gap-2 min-w-[120px]">
              <Volume className="h-3.5 w-3.5 text-muted-foreground" />
              <div className="flex-1">
                <Label htmlFor="volume-slider" className="text-xs text-muted-foreground">
                  Głośność: {Math.round(settings.volume * 100)}%
                </Label>
                <input
                  id="volume-slider"
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={settings.volume}
                  onChange={(e) => setSettings({ volume: parseFloat(e.target.value) })}
                  className="w-full h-1.5 bg-muted rounded-lg appearance-none cursor-pointer accent-foreground/20"
                />
              </div>
            </div>

            {/* Pause Duration */}
            <div className="flex items-center gap-2 min-w-[120px]">
              <Pause className="h-3.5 w-3.5 text-muted-foreground" />
              <div className="flex-1">
                <Label htmlFor="pause-slider" className="text-xs text-muted-foreground">
                  Przerwa: {settings.pauseDuration}ms
                </Label>
                <input
                  id="pause-slider"
                  type="range"
                  min="0"
                  max="1000"
                  step="50"
                  value={settings.pauseDuration}
                  onChange={(e) => setSettings({ pauseDuration: parseInt(e.target.value) })}
                  className="w-full h-1.5 bg-muted rounded-lg appearance-none cursor-pointer accent-foreground/20"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
