import { NavLink, useNavigate } from "react-router-dom";
import styles from "./Header.module.css";
import logo from "@/assets/logo-modified.png";
import { useUser } from "@/contexts/UserContext";
import SearchBar from "./SearchBar";
import { useState } from "react";

export default function Header() {
  const { user, setUser } = useUser();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState<boolean>(false);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
    navigate("/login");
  };

  return (
    <div className={styles.mainHeader}>
      <div className={styles.left}>
        <NavLink to="/">
          <img src={logo} alt="TuneQuest" className={styles.image} />
        </NavLink>
      </div>

      <div className={styles.center}>
        <SearchBar />
      </div>

      <div className={styles.right}>
        <div className={styles.desktopMenu}>
          <NavLink to="/companion">
            <button className={styles.btnHeader}>
              <span>Companion</span>
            </button>
          </NavLink>
          <NavLink to="/favorites">
            <button className={styles.btnHeader}>
              <span>Favorites</span>
            </button>
          </NavLink>
          {user ? (
            <button className={styles.btnHeader} onClick={handleLogout}>
              Log Out
            </button>
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
        <button
          className={styles.hamburger}
          onClick={() => setMenuOpen((prev) => !prev)}
          aria-label="Toggle menu"
        >
          ☰
        </button>
      </div>
      {menuOpen && (
        <div className={styles.mobileMenu}>
          <ul className={styles.dropdownList}>
            <li>
              <NavLink to="/companion" onClick={() => setMenuOpen(false)}>
                Companion
              </NavLink>
            </li>
            <li>
              <NavLink to="/favorites" onClick={() => setMenuOpen(false)}>
                Favorites
              </NavLink>
            </li>
            {user ? (
              <button
                onClick={() => {
                  handleLogout();
                  setMenuOpen(false);
                }}
                className={styles.dropdownButton}
              >
                Log Out
              </button>
            ) : (
              <>
                <li>
                  <NavLink to="/signup" onClick={() => setMenuOpen(false)}>
                    Sign Up
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/login" onClick={() => setMenuOpen(false)}>
                    Login
                  </NavLink>
                </li>
              </>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
