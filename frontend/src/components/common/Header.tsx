import { NavLink, useNavigate } from "react-router-dom";
import styles from "./Header.module.css";
import logo from "../assets/logo-modified.png";
import { useUser } from "../contexts/UserContext";
import SearchBar from "./SearchBar.tsx";

export default function Header() {
  const { user, setUser } = useUser();
  const navigate = useNavigate();

  return (
    <div className={styles.mainHeader}>
      <NavLink to="/">
        <img src={logo} alt="TuneQuest" className={styles.image} />
      </NavLink>
      <SearchBar />
      {user ? (
        <>
          <NavLink to="/profile">
            <button className={styles.btnHeader}>
              <span>Profile</span>
            </button>
          </NavLink>
          <div>
            <button
              className={styles.btnHeader}
              onClick={() => {
                localStorage.removeItem("access_token");
                setUser(null);
                navigate("/login");
              }}
            >
              Log Out
            </button>
          </div>
        </>
      ) : (
        <>
          <NavLink to="/companion">
            <button className={styles.btnHeader}>
              <span>Companion</span>
            </button>
          </NavLink>
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
