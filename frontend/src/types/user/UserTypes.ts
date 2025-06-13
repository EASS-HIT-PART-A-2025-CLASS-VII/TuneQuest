import type { RecommendationItem } from "@/types/ai/AITypes";

export interface SpotifyFavorites {
tracks: RecommendationItem[];
artists: RecommendationItem[];
albums: RecommendationItem[];
}

export interface User {
id: string;
username: string;
email: string;
}

export interface UserContextType {
  user: User | null;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
  loading: boolean;
}

export interface FormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export interface FormErrors {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}