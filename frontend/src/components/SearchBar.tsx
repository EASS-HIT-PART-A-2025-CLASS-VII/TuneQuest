import styles from "./SearchBar.module.css";
import { useState, useEffect } from "react";
import { NavLink } from "react-router";
import { useNavigate } from "react-router-dom";
import fetchTracks from "../api/fetchTracks";

export default function SearchBar() {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState([]);

  const navigate = useNavigate();

  // Debounce search term
  useEffect(() => {
    const timeout = setTimeout(() => {
      if (search.trim() !== "") {
        fetchTracks(search).then((tracks) => setResults(tracks));
      } else {
        setResults([]);
      }
    }, 400); // 400ms debounce

    return () => clearTimeout(timeout);
  }, [search]);

  function checkKey(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      navigate(`/search?query=${encodeURIComponent(search)}`);
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
      {results.length > 0 && (
        <div className={styles.dropdown}>
          {results.slice(0, 5).map((track: any) => (
            <div key={track.id} className={styles.card}>
              {track.album?.images?.[0]?.url && (
                <img
                  src={track.album.images[0].url}
                  alt={track.name}
                  className={styles.image}
                />
              )}
              <h3 className={styles.title}>{track.name}</h3>
              <p className={styles.artist}>
                {track.album?.artists?.[0]?.name ?? "Unknown Artist"}
              </p>
            </div>
          ))}
          <NavLink to="/search">
            <button className={styles.seeAll}>
              <span>See all</span>
            </button>
          </NavLink>
        </div>
      )}
    </div>
  );
}
