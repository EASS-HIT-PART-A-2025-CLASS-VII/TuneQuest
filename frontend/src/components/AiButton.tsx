import styles from "./AiButton.module.css";
import { useState } from "react";
import { TrackCard, ArtistCard, AlbumCard } from "./Cards";

type AiButtonProps = {
  type: string;
  name: string;
};

type RecommendationItem = {
  id: string;
  name: string;
  type: string;
  image: string;
  url: string;
};

export function AiButton({ type, name }: AiButtonProps) {
  const [results, setResults] = useState<RecommendationItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
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
    <div>
      <button
        onClick={handleClick}
        className={styles.button}
        disabled={loading}
      >
        {loading ? "Loading..." : "Ask AI"}
      </button>
      {error && <p className={styles.error}>{error}</p>}
      {results.length > 0 && (
        <div>
          {type === "track" && (
            <div>
              {results.map((item) => (
                <TrackCard key={item.id} track={item} />
              ))}
            </div>
          )}
          {type === "artist" && (
            <div>
              {results.map((item) => (
                <ArtistCard key={item.id} artist={item} />
              ))}
            </div>
          )}

          {type === "album" && (
            <div>
              {results.map((item) => (
                <AlbumCard key={item.id} album={item} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
