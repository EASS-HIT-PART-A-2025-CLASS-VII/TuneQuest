import { NavLink } from "react-router-dom";
import styles from "./Cards.module.css";

export function TrackCard({ track }: { readonly track: any }) {
  return (
    <NavLink to={`/track/${track.id}`} className={styles.card}>
      <img
        src={track.album.images[0]?.url}
        alt={track.name}
        className={styles.image}
      />
      <div className={styles.info}>
        <h4 className={styles.title}>{track.name}</h4>
        <p className={styles.subtitle}>
          {track.artists.map((a: any) => a.name).join(", ")}
        </p>
      </div>
    </NavLink>
  );
}

export function CompactTrackCard({ track }: { readonly track: any }) {
  return (
    <NavLink to={`/track/${track.id}`} className={styles.card}>
      <p>{track.track_number}</p>
      <div className={styles.info}>
        <h4 className={styles.title}>{track.name}</h4>
        <p className={styles.subtitle}>
          {track.artists.map((a: any) => a.name).join(", ")}
        </p>
      </div>
    </NavLink>
  );
}

export function AlbumCard({ album }: { readonly album: any }) {
  return (
    <NavLink to={`/album/${album.id}`} className={styles.card}>
      <img
        src={album.images[0]?.url}
        alt={album.name}
        className={styles.image}
      />
      <div className={styles.info}>
        <h4 className={styles.title}>{album.name}</h4>
        <p className={styles.subtitle}>
          {album.artists.map((a: any) => a.name).join(", ")}
        </p>
      </div>
    </NavLink>
  );
}

export function ArtistCard({ artist }: { readonly artist: any }) {
  return (
    <NavLink to={`/artist/${artist.id}`} className={styles.card}>
      <img
        src={artist.images[0]?.url ?? "/default-artist.png"}
        alt={artist.name}
        className={styles.image}
      />
      <div className={styles.info}>
        <h4 className={styles.title}>{artist.name}</h4>
      </div>
    </NavLink>
  );
}
