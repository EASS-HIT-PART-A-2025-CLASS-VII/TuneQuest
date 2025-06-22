import styles from "./Home.module.css";
import AiHomeButton from "@/components/common/AiHomeButton";

export default function Home() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>🎵 Welcome to TuneQuest</h1>
      <p className={styles.description}>
        Discover and manage your favorite tracks with ease.
      </p>
      <AiHomeButton />
    </div>
  );
}
