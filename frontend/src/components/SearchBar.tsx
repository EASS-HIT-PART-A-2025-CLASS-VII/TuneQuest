import styles from "./SearchBar.module.css";
import { useState, useEffect } from "react";
import { NavLink, useNavigate, useLocation } from "react-router-dom";
import fetchSearchResults from "../api/fetchSearchResults";
import { TrackCard, AlbumCard, ArtistCard } from "./Cards.tsx";

export default function SearchBar() {
  const [search, setSearch] = useState("");
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
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    setSearch("");
  }, [location.pathname]);

  useEffect(() => {
    if (search.trim() === "") {
      setResults({ tracks: [], albums: [], artists: [] });
      setLoading(false);
      return;
    }

    setLoading(true);
    const timeout = setTimeout(() => {
      fetchSearchResults(search)
        .then((data) => setResults(data))
        .finally(() => setLoading(false));
    }, 400);

    return () => clearTimeout(timeout);
  }, [search]);

  function checkKey(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      navigate(`/search?query=${encodeURIComponent(search)}`);
      setSearch("");
    }
  }

  return (
    <div className={styles.container}>
      <input
        type="search"
        className={styles.searchBar}
        placeholder="Search"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        onKeyDown={checkKey}
      />

      {loading && <div className={styles.loading}>Loading...</div>}

      {!loading && results[type].length > 0 && (
        <div className={styles.dropdown}>
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

          {type === "tracks" &&
            results.tracks
              .slice(0, 5)
              .map((track) => <TrackCard key={track.id} track={track} />)}

          {type === "albums" &&
            results.albums
              .slice(0, 5)
              .map((album) => <AlbumCard key={album.id} album={album} />)}

          {type === "artists" &&
            results.artists
              .slice(0, 5)
              .map((artist) => <ArtistCard key={artist.id} artist={artist} />)}

          <NavLink
            to={`/search?query=${encodeURIComponent(search)}`}
            onClick={() => {
              setLoading(false);
              setSearch("");
            }}
          >
            <button className={styles.seeAll}>
              <span>See all</span>
            </button>
          </NavLink>
        </div>
      )}
    </div>
  );
}
