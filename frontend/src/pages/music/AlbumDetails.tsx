import { useParams, NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import styles from "./AlbumDetails.module.css";
import { NonImageTrackCard } from "@/components/features/Cards";
import { fetchDeezerGenres } from "@/api/deezer";
import { AiButton } from "@/components/common/AiButton";
import { ImSpinner2 } from "react-icons/im";
import shared from "@/styles/shared.module.css";
import { MdFavorite, MdFavoriteBorder } from "react-icons/md";
import { useUser } from "@/contexts/UserContext";
import type { FullAlbum } from "@/types/music/MusicTypes";
import { fetchWithService } from "@/utils/api";

export default function AlbumDetails() {
  const { id } = useParams<{ id: string }>();
  const [album, setAlbum] = useState<FullAlbum | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [genres, setGenres] = useState<string[]>([]);
  const [favorite, setFavorite] = useState(false);
  const { user } = useUser();
  const token = localStorage.getItem("access_token");

  useEffect(() => {
    setLoading(true);
    fetchWithService(`/spotify/album/${id}`,'MUSIC_SERVICE')
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch album");
        return res.json();
      })
      .then((data) => setAlbum(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));

    if (user) {
      fetchWithService(`/favorites/${id}?type=album`,'MUSIC_SERVICE', {
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
  }, [id, user?.id]);

  useEffect(() => {
    if (album) {
      const albumName = album.name;
      const artistName = album.artists[0].name;
      fetchDeezerGenres(albumName, artistName).then((deezerGenres) => {
        setGenres(deezerGenres);
      });
    }
  }, [album]);

  const handleFavorite = async () => {
    if (!user) {
      alert("You need to be logged in to use that feature");
      return;
    }

    try {
      let response;
      if (favorite) {
        response = await fetchWithService(`/favorites/${id}?type=album`,'MUSIC_SERVICE', {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
            },
          }
        );
      } else {
        response = await fetchWithService(`/favorites?spotify_id=${id}&type=album`,'MUSIC_SERVICE', {
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
  if (!loading && !album) return null;

  return (
    <div className={styles.container}>
      {loading && (
        <div className={shared.loading} aria-live="polite" aria-busy="true">
          <ImSpinner2 />
        </div>
      )}

      {!loading && album && (
        <>
          <section className={styles.mainInfo} aria-label="Album information">
            <div>
              {album.images?.[0]?.url && (
                <img
                  src={album.images[0].url}
                  alt={`Album cover for ${album.name}`}
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
                {album.artists.map((artist) => (
                  <span key={artist.id}>
                    <NavLink
                      className={styles.navigate}
                      to={`/artist/${artist.id}`}
                    >
                      {artist.name}
                    </NavLink>
                    {album.artists.indexOf(artist) < album.artists.length - 1 && ", "}
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

              <p>Genres: {genres.length > 0 ? genres.join(", ") : "Unknown"}</p>

              <button
                className={`${shared.favoriteButton} ${
                  favorite ? shared.favorited : ""
                }`}
                onClick={() => {
                  if (user) {
                    handleFavorite();
                  } else {
                    alert("You need to be logged in to use that feature");
                  }
                }}
                aria-pressed={favorite}
                aria-label={
                  favorite ? "Remove from favorites" : "Add to favorites"
                }
              >
                {favorite ? <MdFavorite /> : <MdFavoriteBorder />}
              </button>
            </div>
          </section>

          {album.tracks?.items?.length > 0 && (
            <section className={styles.tracks} aria-label="Album tracks">
              {album.tracks.items.map((track) => (
                <NonImageTrackCard key={track.id} track={track} />
              ))}
            </section>
          )}

          <p>Release Date: {album.release_date}</p>
        </>
      )}
    </div>
  );
}
