import styles from "./SearchBar.module.css";
import { useState, useEffect } from "react";
import { NavLink } from "react-router";
import { useNavigate } from "react-router-dom";
import fetchTracks from "../api/fetchTracks";
import TrackCard from "./TrackCard";

export default function SearchBar() {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Debounce search term
  useEffect(() => {
    if (search.trim() === "") {
      setResults([]);
      setLoading(false);
      return;
    }

    setLoading(true);
    const timeout = setTimeout(() => {
      fetchTracks(search)
        .then((tracks) => setResults(tracks))
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
      {!loading && results.length > 0 && (
        <div className={styles.dropdown}>
          {results.slice(0, 5).map((track: any) => (
            <NavLink
              key={track.id}
              to={`/track/${track.id}`}
              onClick={() => setSearch("")}
            >
              <TrackCard track={track} />
            </NavLink>
          ))}
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
      )}{" "}
    </div>
  );
}
