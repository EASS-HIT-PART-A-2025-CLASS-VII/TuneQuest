import styles from "./SignUp.module.css";
import { useState } from "react";

export default function SignUp() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [errors, setErrors] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  function validate(name: string, value: string) {
    let error = "";

    if (name === "username" && value.trim().length < 3) {
      error = "⚠️ Username must be at least 3 characters.";
    }

    if (name === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      error = "⚠️ Invalid email address.";
    }

    if (name === "password") {
      if (value.length < 6) {
        error = "⚠️ Password must be at least 6 characters.";
      } else if (!/[A-Z]/.test(value) || !/\d/.test(value)) {
        error = "⚠️ Include at least 1 number and 1 uppercase letter.";
      }
    }

    if (name === "confirmPassword" && value !== formData.password) {
      error = "⚠️ Passwords do not match.";
    }

    setErrors((prev) => ({ ...prev, [name]: error }));
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    validate(name, value);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    console.log("Form data submitted:", formData);
    // Send to backend here
  }

  return (
    <form onSubmit={handleSubmit} className={styles.SignUpForm}>
      <div className={styles.SignUpContainer}>
        <h2 className={styles.Title}>Sign Up</h2>

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
        {errors.username && <p className={styles.error}>{errors.username}</p>}

        <label htmlFor="email" className={styles.InputName}>
          Email:
        </label>
        <input
          id="email"
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className={styles.InputBar}
        />
        {errors.email && <p className={styles.error}>{errors.email}</p>}

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
        {errors.password && <p className={styles.error}>{errors.password}</p>}

        <label htmlFor="passwordRep" className={styles.InputName}>
          Repeat Password:
        </label>
        <input
          id="passwordRep"
          type="password"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
          className={styles.InputBar}
        />
        {errors.confirmPassword && (
          <p className={styles.error}>{errors.confirmPassword}</p>
        )}

        <button type="submit" className={styles.Submit}>
          Create Account
        </button>
      </div>
    </form>
  );
}
