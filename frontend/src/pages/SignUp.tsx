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
    const trimmedValue = value.trim();

    switch (name) {
      case "username":
        if (trimmedValue.length < 3) {
          error = "⚠️ Username must be at least 3 characters";
        } else if (trimmedValue.length > 20) {
          error = "⚠️ Username must not be longer than 20 characters";
        }
        break;

      case "email":
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmedValue)) {
          error = "⚠️ Invalid email address.";
        }
        break;

      case "password":
        if (value.length < 8) {
          error = "⚠️ Password must be at least 8 characters.";
        } else if (value.length > 20) {
          error = "⚠️ Password must not be longer than 20 characters";
        } else if (!/[A-Z]/.test(value) || !/\d/.test(value)) {
          error = "⚠️ Include at least 1 number and 1 uppercase letter.";
        }
        break;

      case "confirmPassword":
        if (value !== formData.password) {
          error = "⚠️ Passwords do not match.";
        }
        break;
    }

    setErrors((prev) => ({ ...prev, [name]: error }));
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    validate(name, value);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    const { confirmPassword, ...newForm } = formData;
    console.log(newForm);
    try {
      const response = await fetch("http://localhost:8000/users/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newForm),
      });
      const data = await response.json();
      if (!response.ok) {
        alert(data.detail ?? "Invalid login");
      } else {
        console.log("Login successful:", data);
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("Something went wrong. Try again later.");
    }
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
