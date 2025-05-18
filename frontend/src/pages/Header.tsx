import { NavLink, useNavigate } from "react-router-dom";
import styles from "./Header.module.css";
import logo from "../assets/logo-modified.png";
import { useUser } from "../contexts/UserContext";

export default function Header() {
  const navigate = useNavigate();
  const { user, setUser } = useUser();

  function handleLogout() {
    localStorage.removeItem("access_token");
    setUser(null);
    navigate("/");
  }

  return (
    <div className={styles.mainHeader}>
      <NavLink to="/">
        <img src={logo} alt="TuneQuest" className={styles.image} />
      </NavLink>

      {user ? (
        <>
          <NavLink to="/profile">
            <button className={styles.btnHeader}>
              <span>Profile</span>
            </button>
          </NavLink>
          <button className={styles.btnHeader} onClick={handleLogout}>
            <span>Logout</span>
          </button>
        </>
      ) : (
        <>
          <NavLink to="/signup">
            <button className={styles.btnHeader}>
              <span>Sign Up</span>
            </button>
          </NavLink>
          <NavLink to="/login">
            <button className={styles.btnHeader}>
              <span>Login</span>
            </button>
          </NavLink>
        </>
      )}
    </div>
  );
}
