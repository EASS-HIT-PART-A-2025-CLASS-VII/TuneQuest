import styles from "./login.module.css";
import { useState } from "react";

export default function LogIn() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    console.log("Form data submitted:", formData);
    // Send to backend here
  }

  return (
    <form onSubmit={handleSubmit} className={styles.LogInForm}>
      <div className={styles.LogInContainer}>
        <h2 className={styles.Title}>Log In</h2>

        <label htmlFor="username" className={styles.InputName}>
          Username:
        </label>
        <input
          id="username"
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
          className={styles.InputBar}
        />

        <label htmlFor="password" className={styles.InputName}>
          Password:
        </label>
        <input
          id="password"
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          className={styles.InputBar}
        />

        <button type="submit" className={styles.Submit}>
          Log In
        </button>
      </div>
    </form>
  );
}
