import styles from "./Search.module.css";
import { useEffect, useState } from "react";
import { useLocation } from "react-router";
import { fetchSearchResults } from "@/api/fetchSearchResults";
import { TrackCard, AlbumCard, ArtistCard } from "@/components/features/Cards";
import { ImSpinner2 } from "react-icons/im";
import shared from "@/styles/shared.module.css";
import type { SearchResults } from "@/types/music/MusicTypes";

export default function Search() {
  const [results, setResults] = useState<SearchResults>({
    tracks: [],
    albums: [],
    artists: [],
  });
  const [loading, setLoading] = useState(false);
  const [type, setType] = useState<"tracks" | "albums" | "artists">("tracks");
  const location = useLocation();

  useEffect(() => {
    const fetchData = async () => {
      const url = new URLSearchParams(location.search);
      const query = url.get("query");
      if (!query) {
        setResults({ tracks: [], albums: [], artists: [] });
        setLoading(false);
        return;
      }

      setLoading(true);
      try {
        const data = await fetchSearchResults(query);
        setResults(data);
      } catch (error) {
        console.error(error);
        setResults({ tracks: [], albums: [], artists: [] });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [location.search]);

  return (
    <div>
      {loading && (
        <div className={shared.loading}>
          <ImSpinner2 />
        </div>
      )}
      {!loading && (
        <>
          <div className={styles.buttonsContainer}>
            <button className={styles.button} onClick={() => setType("tracks")}>
              Tracks
            </button>
            <button className={styles.button} onClick={() => setType("albums")}>
              Albums
            </button>
            <button
              className={styles.button}
              onClick={() => setType("artists")}
            >
              Artists
            </button>
          </div>

          <div className={styles.container}>
            {type === "tracks" && (
              <>
                <div className={styles.column}>
                  {results.tracks
                    .filter((_, index) => index % 2 === 0)
                    .map((track) => (
                      <TrackCard key={track.id} track={track} />
                    ))}
                </div>
                <div className={styles.column}>
                  {results.tracks
                    .filter((_, index) => index % 2 === 1)
                    .map((track) => (
                      <TrackCard key={track.id} track={track} />
                    ))}
                </div>
              </>
            )}
            {type === "albums" && (
              <>
                <div className={styles.column}>
                  {results.albums
                    .filter((_, index) => index % 2 === 0)
                    .map((album) => (
                      <AlbumCard key={album.id} album={album} />
                    ))}
                </div>
                <div className={styles.column}>
                  {results.albums
                    .filter((_, index) => index % 2 === 1)
                    .map((album) => (
                      <AlbumCard key={album.id} album={album} />
                    ))}
                </div>
              </>
            )}
            {type === "artists" && (
              <>
                <div className={styles.column}>
                  {results.artists
                    .filter((_, index) => index % 2 === 0)
                    .map((artist) => (
                      <ArtistCard key={artist.id} artist={artist} />
                    ))}
                </div>
                <div className={styles.column}>
                  {results.artists
                    .filter((_, index) => index % 2 === 1)
                    .map((artist) => (
                      <ArtistCard key={artist.id} artist={artist} />
                    ))}
                </div>
              </>
            )}
          </div>
        </>
      )}
    </div>
  );
}
