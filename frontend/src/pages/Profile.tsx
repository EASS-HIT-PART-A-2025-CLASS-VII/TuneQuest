import styles from "./Profile.module.css";
import userImage from "../assets/user-image.webp";

export default function Profile() {
  return (
    <div className={styles.profileContainer}>
      <div className={styles.first}>
        <img src={userImage} alt="" className={styles.userImage} />
        <p>Full name: </p>
        <p>Username: </p>
        <p>Email: </p>
      </div>
    </div>
  );
}
