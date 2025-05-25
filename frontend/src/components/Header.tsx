import { NavLink } from "react-router-dom";
import styles from "./Header.module.css";
import logo from "../assets/logo-modified.png";
import LogoutButton from "./LogoutButton";
import { useUser } from "../contexts/UserContext";
import logoutButtonStyles from "./LogoutButton.module.css";
import SearchBar from "./SearchBar.tsx";

export default function Header() {
  const { user } = useUser();

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
          <LogoutButton className={logoutButtonStyles.logoutButtonHeader} />
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
