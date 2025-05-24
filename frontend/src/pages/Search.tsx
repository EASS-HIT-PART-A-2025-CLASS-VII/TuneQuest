import styles from "./Search.module.css";
import { useEffect, useState } from "react";
import { useLocation } from "react-router";
import fetchTracks from "../api/fetchTracks";

export default function Search() {
  const [results, setResults] = useState([]);
  const location = useLocation();

  useEffect(() => {
    const fetchData = async () => {
      const url = new URLSearchParams(location.search);
      const query = url.get("query");
      if (query) {
        const data = await fetchTracks(query);
        setResults(data);
      }
    };
    fetchData();
  }, [location.search]);
  return (
    <div>
      {results.slice(0, 5).map((track: any) => (
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
  );
}
