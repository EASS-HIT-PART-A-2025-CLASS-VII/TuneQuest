import styles from "./Search.module.css";
import { useState, useEffect } from "react";

export default function Search() {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState([]);

  // Debounce search term
  useEffect(() => {
    const timeout = setTimeout(() => {
      if (search.trim() !== "") {
        fetchTracks(search);
      } else {
        setResults([]);
      }
    }, 400); // 400ms debounce

    return () => clearTimeout(timeout);
  }, [search]);

  async function fetchTracks(query: string) {
    try {
      const response = await fetch(
        `http://localhost:8000/spotify/search?query=${encodeURIComponent(
          query
        )}`,
        {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        }
      );

      if (!response.ok) {
        alert("No tracks found");
        return;
      }

      const tracks = await response.json();
      setResults(tracks); // store and use results
    } catch (error) {
      console.error("Search error:", error);
      alert("Something went wrong. Try again later.");
    }
  }

  return (
    <div className={styles.container}>
      <input
        type="search"
        className={styles.search}
        placeholder="Search"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      {results.length > 0 && (
        <div className={styles.dropdown}>
          {results.map((track: any) => (
            <div key={track.id} className={styles.card}>
              {track.album?.images?.[0]?.url && (
                <img
                  src={track.album.images[0].url}
                  alt={track.name}
                  className={styles.image}
                />
              )}
              <h3 className={styles.title}>{track.name}</h3>
              <p className={styles.artist}>
                {track.album?.artists?.[0]?.name ?? "Unknown Artist"}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
