import styles from "./TrackCard.module.css";

export default function TrackCard({ track }: { readonly track: any }) {
  return (
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
  );
}
