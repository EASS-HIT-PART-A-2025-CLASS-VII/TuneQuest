import { NavLink } from "react-router-dom";
import styles from "./Header.module.css";
import logo from "../assets/logo-modified.png";
import LogoutButton from "../components/LogoutButton";
import { useUser } from "../contexts/UserContext";

export default function Header() {
  const { user } = useUser();

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
          <LogoutButton />
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
