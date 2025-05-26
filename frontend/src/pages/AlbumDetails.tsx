import { useParams, NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import styles from "./AlbumDetails.module.css";
import TrackCard from "../components/TrackCard"; // adjust if needed

export default function AlbumDetails() {
  const { id } = useParams<{ id: string }>();
  const [album, setAlbum] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch(`http://localhost:8000/spotify/album/${id}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch album");
        return res.json();
      })
      .then((data) => setAlbum(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (error) return <p>Error: {error}</p>;
  if (!loading && !album) return null;

  return (
    <div className={styles.container}>
      {loading && <div className={styles.loading}>Loading...</div>}
      {!loading && album && (
        <>
          <h2>{album.name}</h2>
          <p>Artists: {album.artists?.map((a: any) => a.name).join(", ")}</p>
          {album.images?.length > 0 && (
            <img
              src={album.images[0].url}
              alt={album.name}
              width={300}
              height="auto"
            />
          )}
          <p>Type: {album.album_type}</p>
          <p>
            Release Year:{" "}
            {album.release_date_precision === "year"
              ? album.release_date
              : new Date(album.release_date).toLocaleDateString()}
          </p>

          <p>Popularity: {album.popularity ?? "N/A"}</p>
          <p>Genres: {album.genres?.join(", ") ?? "N/A"}</p>

          {album.tracks?.items?.length > 0 && (
            <div className={styles.tracks}>
              <h3>Tracks:</h3>
              {album.tracks.items.map((track: any) => (
                <NavLink key={track.id} to={`/track/${track.id}`}>
                  <TrackCard track={track} />
                </NavLink>
              ))}
            </div>
          )}
          <p>Release Date: {album.release_date}</p>
        </>
      )}
    </div>
  );
}
