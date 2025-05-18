import { useUser } from "../contexts/UserContext";
import { useNavigate } from "react-router-dom";
import styles from "./LogoutButton.module.css";

export default function LogoutButton() {
  const { setUser } = useUser();
  const navigate = useNavigate();

  function logout() {
    localStorage.removeItem("access_token");
    setUser(null);
    navigate("/login");
  }

  return (
    <button onClick={logout} className={styles.logoutButton}>
      Log Out
    </button>
  );
}
