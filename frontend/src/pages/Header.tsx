import { NavLink } from "react-router-dom";
import styles from "./Header.module.css";
import logo from "../assets/logo-modified.png";

export default function Header() {
  return (
    <div className={styles.mainHeader}>
      <NavLink to="/">
        <img src={logo} alt="TuneQuest" className={styles.image} />
      </NavLink>
      <NavLink to="/profile">
        <button className={styles.btnHeader}>
          <span>Profile</span>
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
    </div>
  );
}
