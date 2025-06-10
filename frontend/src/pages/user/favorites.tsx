import styles from "./favorites.module.css";
import { TrackCard, ArtistCard, AlbumCard } from "@/components/features/Cards";
import { useState, useEffect } from "react";
import { ImSpinner2 } from "react-icons/im";
import shared from "@/styles/shared.module.css";
import { useUser } from "@/contexts/UserContext";

/**
 * Interface for a recommendation item
 */
interface RecommendationItem {
  /**
   * Unique identifier for the item
   */
  id: string;
  /**
   * Name of the item
   */
  name: string;
  /**
   * Type of the item (e.g. track, artist, album)
   */
  type: string;
  /**
   * Image URL for the item
   */
  image: string;
  /**
   * URL for the item
   */
  url: string;
}

/**
 * Interface for Spotify favorites data
 */
interface SpotifyFavorites {
  /**
   * Array of track recommendation items
   */
  tracks: RecommendationItem[];
  /**
   * Array of artist recommendation items
   */
  artists: RecommendationItem[];
  /**
   * Array of album recommendation items
   */
  albums: RecommendationItem[];
}

/**
 * Favorites page component
 */
export default function Favorites() {
  /**
   * State for storing favorites data
   */
  const [favorites, setFavorites] = useState<SpotifyFavorites>({
    tracks: [],
    artists: [],
    albums: [],
  });
  /**
   * State for loading indicator
   */
  const [loading, setLoading] = useState(false);
  /**
   * State for current type of favorites to display
   */
  const [type, setType] = useState<"tracks" | "albums" | "artists">("tracks");
  /**
   * State for error message
   */
  const [error, setError] = useState<string | null>(null);
  /**
   * Get user data from context
   */
  const { user } = useUser();
  /**
   * Get access token from local storage
   */
  const token = localStorage.getItem("access_token");

  /**
   * Effect hook to fetch favorites data on mount
   */
  useEffect(() => {
    const fetchFavorites = async () => {
      if (!user) return;
      try {
        setLoading(true);
        const resFavs = await fetch(`http://localhost:8000/favorites/spotify`, {
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
