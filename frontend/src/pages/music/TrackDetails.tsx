import { useParams, NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import styles from "./TrackDetails.module.css";
import { fetchDeezerGenres, fetchDeezerPreviewUrl } from "@/api/deezer";
import { AiButton } from "@/components/common/AiButton";

export default function TrackDetails() {
  const { id } = useParams<{ id: string }>();
  const [track, setTrack] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [genres, setGenres] = useState<string[]>([]);
  const [deezerPreviewUrl, setDeezerPreviewUrl] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch(`http://localhost:8000/spotify/track/${id}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch track");
        return res.json();
      })
      .then((data) => setTrack(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  useEffect(() => {
    if (track) {
      const trackName = track.name;
      const albumName = track.album.name;
      const artistName = track.artists[0].name;
      fetchDeezerGenres(albumName, artistName).then((deezerGenres) => {
        setGenres(deezerGenres);
      });
      fetchDeezerPreviewUrl(trackName, artistName).then((url) => {
        setDeezerPreviewUrl(url.length > 0 ? url[0] : null);
      });
    }
  }, [track]);

  if (error) return <p>Error: {error}</p>;
  if (!loading && !track) return null;

  function formatDuration(ms: number): string {
    const totalSec = Math.floor(ms / 1000);
    const min = Math.floor(totalSec / 60);
    const sec = totalSec % 60;
    return `${min}:${sec < 10 ? "0" : ""}${sec}`;
  }

  return (
    <div className={styles.container}>
      {loading && <div className={styles.loading}>Loading...</div>}
      {!loading && track && (
        <div className={styles.mainInfo}>
          <div>
            {track.album.images?.length > 0 && (
              <img
                src={track.album.images[0].url}
                alt={track.album.name}
                className={styles.albumImage}
                width={300}
                height="auto"
              />
            )}
            <AiButton type="track" name={track.name} />
          </div>
          <div>
            <h2>{track.name}</h2>
            <p>
              {track.artists.map((a: any, idx: number) => (
                <span key={a.id}>
                  <NavLink className={styles.navigate} to={`/artist/${a.id}`}>
                    {a.name}
                  </NavLink>
                  {idx < track.artists.length - 1 ? ", " : ""}
                </span>
              ))}
            </p>
            <NavLink
              className={styles.navigate}
              to={`/album/${track.album.id}`}
            >
              <p>Album: {track.album.name}</p>
            </NavLink>
            {genres.length > 0 ? (
              <p>Genres: {genres?.join(", ") ?? "N/A"}</p>
            ) : (
              <p>Genres: Unknown</p>
            )}
            <p>Duration: {formatDuration(track.duration_ms)}</p>
            <p>Popularity: {track.popularity}</p>
            {deezerPreviewUrl ? (
              <audio className={styles.audio} controls src={deezerPreviewUrl} />
            ) : (
              <p>No preview available</p>
            )}{" "}
          </div>
        </div>
      )}
    </div>
  );
}
