import { useParams, NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import styles from "./TrackDetails.module.css";
import { fetchDeezerGenres, fetchDeezerPreviewUrl } from "@/api/deezer";
import { AiButton } from "@/components/common/AiButton";
import { ImSpinner2 } from "react-icons/im";
import shared from "@/styles/shared.module.css";
import { MdFavorite, MdFavoriteBorder } from "react-icons/md";
import { useUser } from "@/contexts/UserContext";
import type { FullTrack } from "@/types/music/MusicTypes";
import { fetchWithService } from "@/utils/api";

export default function TrackDetails() {
  const { id } = useParams<{ id: string }>();
  const [track, setTrack] = useState<FullTrack | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [genres, setGenres] = useState<string[]>([]);
  const [deezerPreviewUrl, setDeezerPreviewUrl] = useState<string | null>(null);
  const [favorite, setFavorite] = useState(false);
  const { user } = useUser();
  const token = localStorage.getItem("access_token");

  useEffect(() => {
    setLoading(true);
    fetchWithService(`/spotify/track/${id}`, "MUSIC_SERVICE")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch track");
        return res.json();
      })
      .then((data) => setTrack(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));

    if (user) {
      fetchWithService(`/favorites/${id}?type=track`, "MUSIC_SERVICE", {
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

  const handleFavorite = async () => {
    if (!user) {
      alert("You need to be logged in to use that feature");
      return;
    }

    try {
      let response;
      if (favorite) {
        response = await fetchWithService(
          `/favorites/${id}?type=track`,
          "MUSIC_SERVICE",
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
      } else {
        response = await fetchWithService(
          `/favorites?spotify_id=${id}&type=track`,
          "MUSIC_SERVICE",
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
  if (!loading && !track) return null;

  function formatDuration(ms: number): string {
    const totalSec = Math.floor(ms / 1000);
    const min = Math.floor(totalSec / 60);
    const sec = totalSec % 60;
    return `${min}:${sec < 10 ? "0" : ""}${sec}`;
  }

  return (
    <div className={styles.container}>
      {loading && (
        <div className={shared.loading}>
          <ImSpinner2 />
        </div>
      )}
      {!loading && track && (
        <section className={styles.upperSection} aria-label="Track information">
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
            </div>
            <div>
              <h2>{track.name}</h2>
              <p>
                {track.artists.map((a) => (
                  <span key={a.id}>
                    <NavLink className={styles.navigate} to={`/artist/${a.id}`}>
                      {a.name}
                    </NavLink>
                    {track.artists.indexOf(a) < track.artists.length - 1
                      ? ", "
                      : ""}
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
              <div className={styles.buttonAndAudio}>
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
                  aria-label={
                    favorite ? "Remove from favorites" : "Add to favorites"
                  }
                >
                  {favorite ? <MdFavorite /> : <MdFavoriteBorder />}
                </button>
                {deezerPreviewUrl ? (
                  <audio
                    className={styles.audio}
                    controls
                    src={deezerPreviewUrl}
                  >
                    <track
                      kind="captions"
                      srcLang="en"
                      src="path/to/your-captions.vtt"
                      label="English"
                      default
                    />
                    Your browser does not support the audio element.
                  </audio>
                ) : (
                  <p>No preview available</p>
                )}
              </div>
            </div>
          </div>
          <AiButton type="track" name={track.name} />
        </section>
      )}
    </div>
  );
}
