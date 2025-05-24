import styles from "./Search.module.css";
import { useEffect, useState } from "react";
import { useLocation, NavLink } from "react-router";
import fetchTracks from "../api/fetchTracks";
import TrackCard from "../components/TrackCard";

export default function Search() {
  const [results, setResults] = useState([]);
  const location = useLocation();

  useEffect(() => {
    const fetchData = async () => {
      const url = new URLSearchParams(location.search);
      const query = url.get("query");
      if (query) {
        const data = await fetchTracks(query);
        setResults(data);
      }
    };
    fetchData();
  }, [location.search]);
  return (
    <div className={styles.container}>
      <div className={styles.column}>
        {results
          .filter((_, index) => index % 2 === 0)
          .map((track: any) => (
            <NavLink key={track.id} to={`/track/${track.id}`}>
              <TrackCard track={track} />
            </NavLink>
          ))}
      </div>
      <div className={styles.column}>
        {results
          .filter((_, index) => index % 2 === 1)
          .map((track: any) => (
            <NavLink key={track.id} to={`/track/${track.id}`}>
              <TrackCard track={track} />
            </NavLink>
          ))}
      </div>
    </div>
  );
}
