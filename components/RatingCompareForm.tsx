"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

interface RatingCompareFormProps {
  placeId: string;
  onSuccess?: () => void;
}

const versionOptions = [
  { value: "adult_full", label: "Dorośli – pełny" },
  { value: "adult_short", label: "Dorośli – skrót" },
  { value: "child_short", label: "Dzieci – skrót" },
];

const ageGroups = [
  { value: "1-10", label: "1-10" },
  { value: "11-20", label: "11-20" },
  { value: "21-30", label: "21-30" },
  { value: "31-40", label: "31-40" },
  { value: "41-50", label: "41-50" },
  { value: "51-60", label: "51-60" },
  { value: "60+", label: "60+" },
];

function VersionSelect({
  name,
  label,
  value,
  onChange,
  index,
}: {
  name: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
  index: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className="space-y-2"
    >
      <Label className="text-xs font-medium text-muted-foreground">{label}</Label>
      <RadioGroup value={value} onValueChange={onChange} className="space-y-1">
        {versionOptions.map((option) => (
          <motion.div
            key={option.value}
            whileHover={{ x: 2 }}
            className="flex items-center gap-2"
          >
            <RadioGroupItem value={option.value} id={`${name}-${option.value}`} />
            <Label
              htmlFor={`${name}-${option.value}`}
              className="text-sm cursor-pointer"
            >
              {option.label}
            </Label>
          </motion.div>
        ))}
      </RadioGroup>
    </motion.div>
  );
}

export function RatingCompareForm({ placeId, onSuccess }: RatingCompareFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    bestOverall: "",
    easiestToUnderstand: "",
    bestForChildren: "",
    bestForQuickLook: "",
    bestForPlanning: "",
    ageGroup: "",
    comment: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch("/api/rate-compare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          placeId,
          ...formData,
        }),
      });

      if (response.ok) {
        setSubmitted(true);
        onSuccess?.();
      }
    } catch (error) {
      console.error("Error submitting comparison:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="border border-border rounded-md p-6 text-center shadow-sm bg-muted/30"
      >
        <p className="text-sm text-muted-foreground">
          ✓ Dziękujemy za wypełnienie ankiety
        </p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="border border-border rounded-md p-6 shadow-sm bg-card"
    >
      <div className="mb-6">
        <h3 className="font-medium mb-1">Ankieta porównawcza</h3>
        <p className="text-sm text-muted-foreground">
          Porównaj przeczytane wersje i wybierz najlepszą w każdej kategorii.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <VersionSelect
          name="bestOverall"
          label="Która wersja jest ogólnie najlepsza?"
          value={formData.bestOverall}
          onChange={(v) => setFormData({ ...formData, bestOverall: v })}
          index={0}
        />

        <VersionSelect
          name="easiestToUnderstand"
          label="Najłatwiejsza do zrozumienia?"
          value={formData.easiestToUnderstand}
          onChange={(v) => setFormData({ ...formData, easiestToUnderstand: v })}
          index={1}
        />

        <VersionSelect
          name="bestForChildren"
          label="Najlepsza dla dzieci?"
          value={formData.bestForChildren}
          onChange={(v) => setFormData({ ...formData, bestForChildren: v })}
          index={2}
        />

        <VersionSelect
          name="bestForQuickLook"
          label="Najlepsza do szybkiego podglądu?"
          value={formData.bestForQuickLook}
          onChange={(v) => setFormData({ ...formData, bestForQuickLook: v })}
          index={3}
        />

        <VersionSelect
          name="bestForPlanning"
          label="Najlepsza do planowania wycieczki?"
          value={formData.bestForPlanning}
          onChange={(v) => setFormData({ ...formData, bestForPlanning: v })}
          index={4}
        />

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="space-y-2"
        >
          <Label className="text-xs font-medium text-muted-foreground">Grupa wiekowa</Label>
          <RadioGroup
            value={formData.ageGroup}
            onValueChange={(v) => setFormData({ ...formData, ageGroup: v })}
            className="flex gap-4 flex-wrap"
          >
            {ageGroups.map((option) => (
              <motion.div
                key={option.value}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center gap-2"
              >
                <RadioGroupItem value={option.value} id={`compare-ageGroup-${option.value}`} />
                <Label htmlFor={`compare-ageGroup-${option.value}`} className="text-xs cursor-pointer">
                  {option.label}
                </Label>
              </motion.div>
            ))}
          </RadioGroup>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35 }}
          className="space-y-2"
        >
          <Label htmlFor="compare-comment" className="text-xs font-medium text-muted-foreground">
            Komentarz (opcjonalnie)
          </Label>
          <Textarea
            id="compare-comment"
            placeholder="Twoje uwagi..."
            value={formData.comment}
            onChange={(e) =>
              setFormData({ ...formData, comment: e.target.value })
            }
            className="min-h-[60px] text-sm resize-none"
          />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          whileHover={{ scale: 1.01 }}
          whileTap={{ scale: 0.99 }}
        >
          <Button
            type="submit"
            disabled={isSubmitting}
            size="sm"
            className="w-full shadow-sm hover:shadow-md transition-shadow"
          >
            {isSubmitting ? "Wysyłanie..." : "Wyślij ankietę"}
          </Button>
        </motion.div>
      </form>
    </motion.div>
  );
}
