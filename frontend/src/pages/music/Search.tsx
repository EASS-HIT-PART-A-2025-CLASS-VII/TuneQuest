import styles from "./Search.module.css";
import { useEffect, useState } from "react";
import { useLocation, NavLink } from "react-router";
import { fetchSearchResults } from "@/api/fetchSearchResults";
import { TrackCard, AlbumCard, ArtistCard } from "@/components/features/Cards";

export default function Search() {
  const [results, setResults] = useState<{
    tracks: any[];
    albums: any[];
    artists: any[];
  }>({
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
      {loading && <div className={styles.loading}>Loading...</div>}
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
                    .map((track: any) => (
                      <TrackCard key={track.id} track={track} />
                    ))}
                </div>
                <div className={styles.column}>
                  {results.tracks
                    .filter((_, index) => index % 2 === 1)
                    .map((track: any) => (
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
                    .map((album: any) => (
                      <NavLink key={album.id} to={`/album/${album.id}`}>
                        <AlbumCard album={album} />
                      </NavLink>
                    ))}
                </div>
                <div className={styles.column}>
                  {results.albums
                    .filter((_, index) => index % 2 === 1)
                    .map((album: any) => (
                      <NavLink key={album.id} to={`/album/${album.id}`}>
                        <AlbumCard album={album} />
                      </NavLink>
                    ))}
                </div>
              </>
            )}
            {type === "artists" && (
              <>
                <div className={styles.column}>
                  {results.artists
                    .filter((_, index) => index % 2 === 0)
                    .map((artist: any) => (
                      <NavLink key={artist.id} to={`/artist/${artist.id}`}>
                        <ArtistCard artist={artist} />
                      </NavLink>
                    ))}
                </div>
                <div className={styles.column}>
                  {results.artists
                    .filter((_, index) => index % 2 === 1)
                    .map((artist: any) => (
                      <NavLink key={artist.id} to={`/artist/${artist.id}`}>
                        <ArtistCard artist={artist} />
                      </NavLink>
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
