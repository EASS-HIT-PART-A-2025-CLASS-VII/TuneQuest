import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import styles from "./ArtistDetails.module.css";
import logo from "../assets/logo.png";
import { CompactAlbumCard, TrackCard } from "../components/Cards";

export default function ArtistDetails() {
  const { id } = useParams<{ id: string }>();
  const [artist, setArtist] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [albums, setAlbums] = useState<any[] | null>(null);
  const [topTracks, setTopTracks] = useState<any[] | null>(null);

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
    fetch(
      `http://localhost:8000/spotify/artist/${id}/albums?include_groups=album,single,appears_on,compilation`
    )
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch albums");
        return res.json();
      })
      .then((data) => setAlbums(data.items))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
    fetch(`http://localhost:8000/spotify/artist/${id}/top-tracks`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch top tracks");
        return res.json();
      })
      .then((data) => setTopTracks(data.tracks))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (error) return <p>Error: {error}</p>;
  if (!loading && !artist) return null;

  return (
    <>
      <div className={styles.container}>
        {loading && <div className={styles.loading}>Loading...</div>}
        {!loading && artist && (
          <div className={styles.mainInfo}>
            <div>
              {artist.images?.length > 0 && (
                <img
                  src={artist.images?.[0]?.url ?? logo}
                  alt={artist.name}
                  className={styles.artistImage}
                  width={300}
                  height="auto"
                />
              )}
            </div>
            <div>
              <h2>{artist.name}</h2>
              <p>Genres: {artist.genres?.join(", ") ?? "N/A"}</p>
              <p>Followers: {artist.followers?.total.toLocaleString()}</p>
              <p>Popularity: {artist.popularity}</p>
            </div>
            <div>
              {Array.isArray(topTracks) &&
                topTracks?.length > 0 &&
                topTracks
                  .slice(0, 5)
                  .map((a: any) => <TrackCard key={a.id} track={a} />)}
            </div>
          </div>
        )}
      </div>
      <div>
        {Array.isArray(albums) &&
          albums?.length > 0 &&
          albums.map((a: any) => <CompactAlbumCard key={a.id} album={a} />)}
      </div>{" "}
    </>
  );
}
