import { NavLink, useNavigate } from "react-router-dom";
import styles from "./Header.module.css";
import logo from "../assets/logo-modified.png";

interface HeaderProps {
  readonly isLoggedIn: boolean;
  readonly setIsLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
}

export default function Header({ isLoggedIn, setIsLoggedIn }: HeaderProps) {
  const navigate = useNavigate();
  function handleLogout() {
    localStorage.removeItem("access_token");
    setIsLoggedIn(false);
    navigate("/");
  }
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
      {isLoggedIn ? (
        <button className={styles.btnHeader} onClick={handleLogout}>
          <span>Logout</span>
        </button>
      ) : (
        <NavLink to="/login">
          <button className={styles.btnHeader}>
            <span>Login</span>
          </button>
        </NavLink>
      )}{" "}
    </div>
  );
}
