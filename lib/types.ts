export interface Place {
  id: string;
  name: string;
  thumbnail: string;
  description: string;
}

export interface Article {
  placeId: string;
  style: string;
  ageTarget: "adult" | "child";
  volume: "full" | "short";
  title: string;
  content: string;
}

export interface SingleRating {
  id: string;
  placeId: string;
  articleStyle: string;
  timestamp: string;
  clarity: number;
  styleMatch: number;
  structure: number;
  usefulness: number;
  length: "too_short" | "just_right" | "too_long";
  enjoyment: number;
  comment?: string;
}

export interface CompareRating {
  id: string;
  placeId: string;
  timestamp: string;
  bestOverall: string;
  easiestToUnderstand: string;
  bestForChildren: string;
  bestForQuickLook: string;
  bestForPlanning: string;
  comment?: string;
}




