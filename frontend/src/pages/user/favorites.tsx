import styles from "./favorites.module.css";
import { TrackCard, ArtistCard, AlbumCard } from "@/components/features/Cards";
import { useState, useEffect } from "react";
import { ImSpinner2 } from "react-icons/im";
import shared from "@/styles/shared.module.css";
import { useUser } from "@/contexts/UserContext";
import type { SpotifyFavorites } from "@/types/user/UserTypes";
import { fetchWithService } from "@/utils/api";


export default function Favorites() {

  const [favorites, setFavorites] = useState<SpotifyFavorites>({
    tracks: [],
    artists: [],
    albums: [],
  });

  const [loading, setLoading] = useState(false);
  const [type, setType] = useState<"tracks" | "albums" | "artists">("tracks");
  const [error, setError] = useState<string | null>(null);
  const { user } = useUser();
  const token = localStorage.getItem("access_token");

  useEffect(() => {
    const fetchFavorites = async () => {
      if (!user) return;
      try {
        setLoading(true);
        const resFavs = await fetchWithService(`/favorites/spotify`,'MUSIC_SERVICE', {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const favs = await resFavs.json();
        setFavorites(favs);
      } catch {
        setError("Failed to fetch favorites");
      } finally {
        setLoading(false);
      }
    };
    fetchFavorites();
  }, [user?.id]);

  return (
    <div className={styles.container}>
      {error && <p className={shared.error}>{error}</p>}
      {loading && (
        <div className={shared.loading}>
          <ImSpinner2 />
        </div>
      )}
      <div className={styles.buttonsContainer}>
        <button className={styles.button} onClick={() => setType("tracks")}>
          Tracks
        </button>
        <button className={styles.button} onClick={() => setType("albums")}>
          Albums
        </button>
        <button className={styles.button} onClick={() => setType("artists")}>
          Artists
        </button>
      </div>

      <div className={styles.mainInfo}>
        {type === "tracks" && (
          <>
            {!loading && favorites?.tracks?.length > 0 && (
              <div className={styles.tracks}>
                <h2>Tracks</h2>
                {favorites.tracks.map((track) => (
                  <TrackCard key={track.id} track={track} />
                ))}
              </div>
            )}
          </>
        )}
        {type === "albums" && (
          <>
            {!loading && favorites?.albums?.length > 0 && (
              <div className={styles.column}>
                <h2>Albums</h2>
                {favorites.albums.map((album) => (
                  <AlbumCard key={album.id} album={album} />
                ))}
              </div>
            )}
          </>
        )}
        {type === "artists" && (
          <>
            {!loading && favorites?.artists?.length > 0 && (
              <div className={styles.column}>
                <h2>Artists</h2>
                {favorites.artists.map((artist) => (
                  <ArtistCard key={artist.id} artist={artist} />
                ))}
              </div>
            )}
          </>
        )}
        {!loading &&
          favorites &&
          !(
            (favorites.tracks && favorites.tracks.length > 0) ||
            (favorites.artists && favorites.artists.length > 0) ||
            (favorites.albums && favorites.albums.length > 0)
          ) && <p className={styles.empty}>No favorites yet.</p>}
      </div>
    </div>
  );
}
