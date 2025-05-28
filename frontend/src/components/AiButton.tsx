import styles from "./AiButton.module.css";
import { useState } from "react";
import { CompactAlbumCard } from "./Cards";

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
  const [recommendation, setRecommendation] = useState<string[]>([]);
  const [results, setResults] = useState<RecommendationItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setError(null);
    setResults([]);
    setRecommendation([]);
    setLoading(true);

    try {
      const prompt = `recommend ${type}s similar to ${name}. Return the names only, dont add words. 5 results. Be creative. I want a combination of popular and niche artists. No introductions, no explanations, no other text.`;

      const aiResponse = await fetch("http://localhost:8000/ai/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, type }),
      });

      if (!aiResponse.ok) throw new Error("Failed to fetch AI recommendations");

      const aiData = await aiResponse.json();
      console.log(aiData);
      const albumIds = aiData.results.map((item: any) => item.id);
      console.log(albumIds);
      setRecommendation(albumIds);

      const queryString = albumIds
        .map((id: string) => `${encodeURIComponent(id)}`)
        .join(",");

      const url = `http://localhost:8000/spotify/albums?ids=${queryString}`;
      // 2. Fetch album data from backend using batch ID request
      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to fetch album details");

      const data = await response.json();
      setResults(data.albums); // adjust this depending on your backend's response structure
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
        <ul>
          {results.map((item) => (
            <li key={item.id}>
              <CompactAlbumCard album={item} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
