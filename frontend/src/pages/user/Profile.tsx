import styles from "./Profile.module.css";
import userImage from "@/assets/user-image.webp";
import { useUser } from "@/contexts/UserContext";
import { useNavigate } from "react-router";
export default function Profile() {
  const { user, setUser } = useUser();
  const navigate = useNavigate();
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
          <button
            className={styles.logoutButtonProfile}
            onClick={() => {
              localStorage.removeItem("access_token");
              setUser(null);
              navigate("/login");
            }}
          >
            Log Out
          </button>
        </div>
      </div>
    </div>
  );
}
