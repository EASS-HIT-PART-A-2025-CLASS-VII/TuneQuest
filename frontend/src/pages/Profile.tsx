import styles from "./Profile.module.css";
import userImage from "../assets/user-image.webp";
import { useUser } from "../contexts/UserContext";
import LogoutButton from "../components/LogoutButton";
import logoutButtonStyles from "../components/LogoutButton.module.css";

export default function Profile() {
  const { user } = useUser();

  if (!user) return <p>No user logged in.</p>;

  return (
    <div className={styles.profileContainer}>
      <div className={styles.first}>
        <img
          src={userImage}
          alt=""
          className={styles.userImage}
          onError={(e) => {
            e.currentTarget.src = "fallback-url-or-icon";
          }}
        />
        <p>Full name: {user.fullName}</p>
        <p>Username: {user.username}</p>
        <p>Email: {user.email}</p>
        <div>
          <LogoutButton className={logoutButtonStyles.logoutButtonProfile} />
        </div>
      </div>
    </div>
  );
}
