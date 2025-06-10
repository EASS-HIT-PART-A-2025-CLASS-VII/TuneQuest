import styles from "./SearchBar.module.css";
import { useState, useEffect } from "react";
import { NavLink, useNavigate, useLocation } from "react-router-dom";
import { fetchSearchResults } from "@/api/fetchSearchResults";
import { TrackCard, AlbumCard, ArtistCard } from "../features/Cards";
import { ImSpinner2 } from "react-icons/im";
import shared from "@/styles/shared.module.css";

interface SearchResult {
  tracks: { id: string; name: string; artists: { id: string; name: string }[] }[];
  albums: { id: string; name: string; artists: { id: string; name: string }[] }[];
  artists: { id: string; name: string }[];
}

export default function SearchBar() {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState<SearchResult>({
    tracks: [],
    albums: [],
    artists: [],
  });
  const [loading, setLoading] = useState(false);
  const [type, setType] = useState("tracks");
  const navigate = useNavigate();
  const location = useLocation();
  const types = ["tracks", "albums", "artists"] as const;

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

  const handleEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      navigate(`/search?query=${encodeURIComponent(search)}`);
      setSearch("");
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.inputWrapper}>
        <input
          type="search"
          className={styles.searchBar}
          placeholder="Search for music..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={handleEnter}
        />

        {loading && (
          <div className={shared.loading}>
            <ImSpinner2 />
          </div>
        )}
      </div>

      {!loading && results[type as keyof SearchResult]?.length > 0 && (
        <div className={styles.dropdown}>
          <div className={styles.tabs}>
            {types.map((t) => (
              <button
                key={t}
                className={`${styles.tab} ${
                  type === t ? styles.activeTab : ""
                }`}
                onClick={() => setType(t)}
              >
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>

          <div className={styles.results}>
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
                .map((artist) => (
                  <ArtistCard key={artist.id} artist={artist} />
                ))}
          </div>

          <NavLink
            to={`/search?query=${encodeURIComponent(search)}`}
            onClick={() => {
              setLoading(false);
              setSearch("");
            }}
          >
            <button className={styles.seeAll}>See all results</button>
          </NavLink>
        </div>
      )}
    </div>
  );
}
