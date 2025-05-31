import styles from "./favorites.module.css";
import { TrackCard, ArtistCard, AlbumCard } from "@/components/features/Cards";
import { useState, useEffect } from "react";
import { ImSpinner2 } from "react-icons/im";
import shared from "@/styles/shared.module.css";
import { useUser } from "@/contexts/UserContext";

type Favorite = {
  id: number;
  user_id: number;
  spotify_id: string;
  type: "track" | "album" | "artist";
};

export default function Favorites() {
  const [favorites, setFavorites] = useState<Favorite[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user } = useUser();

  useEffect(() => {
    const fetchFavorites = async () => {
      if (!user) return;
      try {
        setLoading(true);

        const resFavs = await fetch(`http://localhost:8000/favorites`);
        const favs = await resFavs.json();

        setFavorites(favs);
      } catch {
        setError("Failed to fetch favorites");
      } finally {
        setLoading(false);
      }
    };

    fetchFavorites();
  }, []);

  return (
    <div className={styles.container}>
      <div>
        <p>Favorites</p>
      </div>
      <div className={styles.mainInfo}>
        {error && <p className={shared.error}>{error}</p>}

        {loading && (
          <div className={shared.loading}>
            <ImSpinner2 />
          </div>
        )}
        {!loading && favorites?.length > 0 && (
          <>
            <div className={styles.tracks}>
              {favorites
                .filter((fav) => fav.type === "track")
                .map((item) => (
                  <TrackCard key={`track-${item.id}`} track={item.spotify_id} />
                ))}{" "}
            </div>
            <div className={styles.artists}>
              {favorites
                .filter((fav) => fav.type === "artist")
                .map((item) => (
                  <ArtistCard
                    key={`artist-${item.id}`}
                    artist={item.spotify_id}
                  />
                ))}{" "}
            </div>
            <div className={styles.album}>
              {favorites
                .filter((fav) => fav.type === "album")
                .map((item) => (
                  <AlbumCard key={`album-${item.id}`} album={item.spotify_id} />
                ))}{" "}
            </div>
          </>
        )}
        {!loading && favorites.length === 0 && (
          <p className={styles.empty}>No favorites yet.</p>
        )}
      </div>
    </div>
  );
}
