import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import styles from "./ArtistDetails.module.css";
import { CompactAlbumCard, TrackCard } from "@/components/features/Cards";
import { AiButton } from "@/components/common/AiButton";
import { ImSpinner2 } from "react-icons/im";
import shared from "@/styles/shared.module.css";
import { MdFavorite, MdFavoriteBorder } from "react-icons/md";
import { useUser } from "@/contexts/UserContext";

interface Artist {
  id: string;
  name: string;
  genres: string[];
  followers: { total: number };
  popularity: number;
  images: Array<{ url: string }>;
}

interface Album {
  id: string;
  name: string;
  images: Array<{ url: string }>;
}

interface Track {
  id: string;
  name: string;
}

export default function ArtistDetails() {
  const { id } = useParams<{ id: string }>();
  const [artist, setArtist] = useState<Artist | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [albums, setAlbums] = useState<Album[] | null>(null);
  const [topTracks, setTopTracks] = useState<Track[] | null>(null);
  const [favorite, setFavorite] = useState(false);
  const { user } = useUser();
  const token = localStorage.getItem("access_token");

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

    if (user) {
      fetch(`http://localhost:8000/favorites/${id}?type=artist`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          setFavorite(Boolean(data.result));
        })
        .catch((err) => setError(err.message));
    }

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
  }, [id, user?.id]);

  const handleFavorite = async () => {
    if (!user) {
      alert("You need to be logged in to use that feature");
      return;
    }

    try {
      let response;
      if (favorite) {
        response = await fetch(
          `http://localhost:8000/favorites/${id}?type=artist`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
      } else {
        response = await fetch(
          `http://localhost:8000/favorites?spotify_id=${id}&type=artist`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
      }

      const data = await response.json();
      if (!data.result) throw new Error("Failed to update favorite");
      setFavorite((prev) => !prev);
      setError(null);
    } catch {
      setError("");
    }
  };

  if (error) return <p>Error: {error}</p>;
  if (!loading && !artist) return null;

  return (
    <div className={styles.container}>
      {loading && (
        <div className={shared.loading}>
          <ImSpinner2 />
        </div>
      )}

      {!loading && artist && (
        <>
          <div className={styles.mainInfo}>
            <div className={styles.leftSide}>
              {artist.images?.[0]?.url && (
                <img
                  src={artist.images[0].url}
                  alt={artist.name}
                  className={styles.artistImage}
                  width={300}
                  height="auto"
                />
              )}
              <AiButton type="artist" name={artist.name} />
            </div>

            <div className={styles.rightSide}>
              <h2>{artist.name}</h2>
              <p>Genres: {artist.genres?.join(", ") ?? "N/A"}</p>
              <p>Followers: {artist.followers?.total.toLocaleString()}</p>
              <p>Popularity: {artist.popularity}</p>
              <button
                className={`${shared.favoriteButton} ${
                  favorite ? shared.favorited : ""
                }`}
                onClick={() => {
                  if (user) handleFavorite();
                  else alert("You need to be logged in to use that feature");
                }}
                aria-label={
                  favorite ? "Remove from favorites" : "Add to favorites"
                }
              >
                {favorite ? <MdFavorite /> : <MdFavoriteBorder />}
              </button>
            </div>
            <div className={styles.topTracksSection}>
              {Array.isArray(topTracks) &&
                topTracks.length > 0 &&
                topTracks
                  .slice(0, 5)
                  .map((track) => <TrackCard key={track.id} track={track} />)}
            </div>
          </div>

          <div className={styles.albumsSection}>
            <h2>Albums</h2>
            {Array.isArray(albums) &&
              albums.length > 0 &&
              albums.map((album) => (
                <CompactAlbumCard key={album.id} album={album} />
              ))}
          </div>
        </>
      )}
    </div>
  );
}
