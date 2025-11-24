"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

interface RatingSingleFormProps {
  placeId: string;
  articleStyle: string;
  onSuccess?: () => void;
}

const ratingLabels = ["1", "2", "3", "4", "5"];

function RatingScale({
  name,
  label,
  value,
  onChange,
}: {
  name: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-2"
    >
      <Label className="text-xs font-medium text-muted-foreground">{label}</Label>
      <RadioGroup
        value={value}
        onValueChange={onChange}
        className="flex gap-1"
      >
        {ratingLabels.map((rating) => (
          <motion.div
            key={rating}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            className="flex flex-col items-center gap-1"
          >
            <RadioGroupItem
              value={rating}
              id={`${name}-${rating}`}
              className="h-8 w-8 border-border"
            />
            <Label
              htmlFor={`${name}-${rating}`}
              className="text-[10px] text-muted-foreground cursor-pointer"
            >
              {rating}
            </Label>
          </motion.div>
        ))}
      </RadioGroup>
    </motion.div>
  );
}

export function RatingSingleForm({
  placeId,
  articleStyle,
  onSuccess,
}: RatingSingleFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    clarity: "",
    styleMatch: "",
    structure: "",
    usefulness: "",
    length: "",
    enjoyment: "",
    comment: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch("/api/rate-single", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          placeId,
          articleStyle,
          ...formData,
        }),
      });

      if (response.ok) {
        setSubmitted(true);
        onSuccess?.();
      }
    } catch (error) {
      console.error("Error submitting rating:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="py-4 text-center border border-border rounded-md bg-muted/30 shadow-sm"
      >
        <p className="text-sm text-muted-foreground">
          ✓ Dziękujemy za ocenę
        </p>
      </motion.div>
    );
  }

  return (
    <motion.form
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      onSubmit={handleSubmit}
      className="space-y-5 bg-card border border-border rounded-md p-6 shadow-sm"
    >
      <RatingScale
        name="clarity"
        label="Zrozumiałość"
        value={formData.clarity}
        onChange={(v) => setFormData({ ...formData, clarity: v })}
      />

      <RatingScale
        name="styleMatch"
        label="Dopasowanie stylu do kategorii"
        value={formData.styleMatch}
        onChange={(v) => setFormData({ ...formData, styleMatch: v })}
      />

      <RatingScale
        name="structure"
        label="Struktura tekstu"
        value={formData.structure}
        onChange={(v) => setFormData({ ...formData, structure: v })}
      />

      <RatingScale
        name="usefulness"
        label="Przydatność turystyczna"
        value={formData.usefulness}
        onChange={(v) => setFormData({ ...formData, usefulness: v })}
      />

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="space-y-2"
      >
        <Label className="text-xs font-medium text-muted-foreground">Długość tekstu</Label>
        <RadioGroup
          value={formData.length}
          onValueChange={(v) => setFormData({ ...formData, length: v })}
          className="flex gap-4"
        >
          {[
            { value: "too_short", label: "Za krótki" },
            { value: "just_right", label: "W sam raz" },
            { value: "too_long", label: "Za długi" },
          ].map((option) => (
            <motion.div
              key={option.value}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center gap-2"
            >
              <RadioGroupItem value={option.value} id={`length-${option.value}`} />
              <Label htmlFor={`length-${option.value}`} className="text-xs cursor-pointer">
                {option.label}
              </Label>
            </motion.div>
          ))}
        </RadioGroup>
      </motion.div>

      <RatingScale
        name="enjoyment"
        label="Przyjemność czytania"
        value={formData.enjoyment}
        onChange={(v) => setFormData({ ...formData, enjoyment: v })}
      />

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15 }}
        className="space-y-2"
      >
        <Label htmlFor="comment" className="text-xs font-medium text-muted-foreground">
          Komentarz (opcjonalnie)
        </Label>
        <Textarea
          id="comment"
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
        transition={{ delay: 0.2 }}
        whileHover={{ scale: 1.01 }}
        whileTap={{ scale: 0.99 }}
      >
        <Button
          type="submit"
          disabled={isSubmitting}
          size="sm"
          className="w-full shadow-sm hover:shadow-md transition-shadow"
        >
          {isSubmitting ? "Wysyłanie..." : "Wyślij ocenę"}
        </Button>
      </motion.div>
    </motion.form>
  );
}
