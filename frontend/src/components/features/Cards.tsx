import { NavLink } from "react-router-dom";
import styles from "./Cards.module.css";

/**
 * Card component for displaying a track with image.
 */
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
        <p className={styles.artist}>
          {track.artists.map((a: any) => a.name).join(", ")}
        </p>
      </div>
    </NavLink>
  );
}

/**
 * Card component for displaying a track without image.
 */
export function NonImageTrackCard({ track }: { readonly track: any }) {
  return (
    <NavLink to={`/track/${track.id}`} className={styles.card}>
      <p>{track.track_number}</p>
      <div className={styles.info}>
        <h4 className={styles.title}>{track.name}</h4>
        <p className={styles.artist}>
          {track.artists.map((a: any) => a.name).join(", ")}
        </p>
      </div>
    </NavLink>
  );
}

/**
 * Card component for displaying an album with full details.
 */
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
        <p className={styles.artist}>
          {album.artists.map((a: any) => a.name).join(", ")}
        </p>
        <p>
          {album.release_date_precision === "year"
            ? album.release_date
            : new Date(album.release_date).getFullYear()}
        </p>
      </div>
    </NavLink>
  );
}

/**
 * Compact card component for displaying an album with minimal details.
 */
export function CompactAlbumCard({ album }: { readonly album: any }) {
  return (
    <NavLink to={`/album/${album.id}`} className={styles.card}>
      <img
        src={album.images[0]?.url}
        alt={album.name}
        className={styles.image}
      />
      <div className={styles.info}>
        <h4 className={styles.title}>{album.name}</h4>
        <p>
          {album.release_date_precision === "year"
            ? album.release_date
            : new Date(album.release_date).getFullYear()}
        </p>
      </div>
    </NavLink>
  );
}

/**
 * Card component for displaying an artist.
 */
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
