import { useParams, NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import styles from "./AlbumDetails.module.css";
import { NonImageTrackCard } from "../components/Cards";
import { fetchDeezerGenres } from "../api/deezer";
import { AiButton } from "../components/AiButton";

export default function AlbumDetails() {
  const { id } = useParams<{ id: string }>();
  const [album, setAlbum] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [genres, setGenres] = useState<string[]>([]);

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

  useEffect(() => {
    if (album) {
      const albumName = album.name;
      const artistName = album.artists[0].name;
      fetchDeezerGenres(albumName, artistName).then((deezerGenres) => {
        setGenres(deezerGenres);
      });
    }
  }, [album]);

  if (error) return <p>Error: {error}</p>;
  if (!loading && !album) return null;

  return (
    <div className={styles.container}>
      {loading && <div className={styles.loading}>Loading...</div>}
      {!loading && album && (
        <>
          <div className={styles.mainInfo}>
            <div>
              {album.images?.length > 0 && (
                <img
                  src={album.images[0].url}
                  alt={album.name}
                  className={styles.albumImage}
                  width={300}
                  height="auto"
                />
              )}
              <AiButton type="album" name={album.name} />
            </div>
            <div>
              <h2>{album.name}</h2>
              <p>
                {album.artists.map((a: any, idx: number) => (
                  <span key={a.id}>
                    <NavLink className={styles.navigate} to={`/artist/${a.id}`}>
                      {a.name}
                    </NavLink>
                    {idx < album.artists.length - 1 ? ", " : ""}
                  </span>
                ))}
              </p>
              <p>Type: {album.album_type}</p>
              <p>
                Release Year:{" "}
                {album.release_date_precision === "year"
                  ? album.release_date
                  : new Date(album.release_date).getFullYear()}
              </p>

              <p>Popularity: {album.popularity ?? "N/A"}</p>
              {genres.length > 0 ? (
                <p>Genres: {genres?.join(", ") ?? "N/A"}</p>
              ) : (
                <p>Genres: Unknown</p>
              )}
            </div>
          </div>
          {album.tracks?.items?.length > 0 && (
            <div className={styles.tracks}>
              {album.tracks.items.map((track: any) => (
                <NonImageTrackCard key={track.id} track={track} />
              ))}
            </div>
          )}
          <p>Release Date: {album.release_date}</p>
        </>
      )}
    </div>
  );
}
