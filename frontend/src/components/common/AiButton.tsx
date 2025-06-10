import styles from "./AiButton.module.css";
import { useState } from "react";
import { TrackCard, ArtistCard, AlbumCard } from "../features/Cards";
import { ImSpinner2 } from "react-icons/im";
import shared from "@/styles/shared.module.css";

interface AiButtonProps {
  readonly type: string;
  readonly name: string;
}

interface RecommendationItem {
  id: string;
  name: string;
  type: string;
  image: string;
  url: string;
}

export function AiButton({ type, name }: AiButtonProps) {
  const [results, setResults] = useState<RecommendationItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAskAi = async () => {
    setError(null);
    setResults([]);
    setLoading(true);

    try {
      const prompt = `recommend ${type}s similar to ${name}. Return the names only, dont add words. 5 results. Be creative. I want a combination of popular and niche ${type}s. No introductions, no explanations, no other text.`;

      const aiResponse = await fetch("http://localhost:8000/ai/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, type }),
      });

      if (!aiResponse.ok) throw new Error("Failed to fetch AI recommendations");

      const aiData = await aiResponse.json();
      const ids = aiData.results.map((item: any) => item.id).join(",");
      let url = "";
      let dataKey = "";

      switch (type) {
        case "album":
          url = `http://localhost:8000/spotify/albums?ids=${ids}`;
          dataKey = "albums";
          break;
        case "track":
          url = `http://localhost:8000/spotify/tracks?ids=${ids}`;
          dataKey = "tracks";
          break;
        case "artist":
          url = `http://localhost:8000/spotify/artists?ids=${ids}`;
          dataKey = "artists";
          break;
        default:
          throw new Error("Unsupported type");
      }

      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to fetch details");

      const data = await response.json();
      setResults(data[dataKey]);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <button
        onClick={handleAskAi}
        className={styles.button}
        disabled={loading}
      >
        Ask AI
      </button>
      {loading && (
        <div className={shared.loading}>
          <ImSpinner2 />
        </div>
      )}
      {error && <p className={styles.error}>{error}</p>}
      {results.length > 0 && (
        <div>
          {type === "track" &&
            results.map((item) => <TrackCard key={item.id} track={item} />)}
          {type === "artist" &&
            results.map((item) => <ArtistCard key={item.id} artist={item} />)}
          {type === "album" &&
            results.map((item) => <AlbumCard key={item.id} album={item} />)}
        </div>
      )}
    </div>
  );
}
