import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import styles from "./ArtistDetails.module.css";

export default function ArtistDetails() {
  const { id } = useParams<{ id: string }>();
  const [artist, setArtist] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch(`http://localhost:8000/spotify/artist/${id}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch artist");
        return res.json();
      })
      .then((data) => setArtist(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (error) return <p>Error: {error}</p>;
  if (!loading && !artist) return null;

  return (
    <div className={styles.container}>
      {loading && <div className={styles.loading}>Loading...</div>}
      {!loading && artist && (
        <>
          <h2>{artist.name}</h2>
          <p>Genres: {artist.genres?.join(", ") ?? "N/A"}</p>
          <p>Followers: {artist.followers?.total.toLocaleString()}</p>
          <p>Popularity: {artist.popularity}</p>
          {artist.images?.length > 0 && (
            <img
              src={artist.images[0].url}
              alt={artist.name}
              width={300}
              height="auto"
            />
          )}
        </>
      )}
    </div>
  );
}
