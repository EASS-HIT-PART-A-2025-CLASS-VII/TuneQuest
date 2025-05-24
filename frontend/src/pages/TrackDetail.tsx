// src/pages/TrackDetail.tsx
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import styles from "./TrackDetail.module.css";
export default function TrackDetail() {
  const { id } = useParams<{ id: string }>();
  const [track, setTrack] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/spotify/track/${id}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch track");
        return res.json();
      })
      .then((data) => setTrack(data))
      .catch((err) => setError(err.message));
  }, [id]);

  if (error) return <p>Error: {error}</p>;
  if (!track) return <p>Loading...</p>;

  return (
    <div className={styles.container}>
      <div>
        <h2>{track.name}</h2>
        <p>{track.artists.map((a: any) => a.name).join(", ")}</p>
        <img src={track.album.images[0]?.url} alt={track.name} width={300} />
      </div>
      <div className={styles.audioContainer}>
        <audio className={styles.audio} controls src={track.preview_url} />
      </div>
    </div>
  );
}
