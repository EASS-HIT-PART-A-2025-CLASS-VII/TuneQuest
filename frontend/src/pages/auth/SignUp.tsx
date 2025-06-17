import styles from "./SignUp.module.css";
import { useState } from "react";
import type { FormData, FormErrors } from "@/types/user/UserTypes";
import { fetchWithService } from "@/utils/api";
import { useNavigate } from "react-router-dom";
import { useUser } from "@/contexts/UserContext";

export default function SignUp() {
  const [formData, setFormData] = useState<FormData>({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [errors, setErrors] = useState<FormErrors>({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const navigate = useNavigate();
  const { setUser } = useUser();

  function validate(name: keyof FormData, value: string) {
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
    validate(name as keyof FormData, value);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    const { confirmPassword, ...newForm } = formData;
    try {
      const response = await fetchWithService("/users/register", "BACKEND", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newForm),
      });

      const data = await response.json();
      if (!response.ok) {
        alert(data.detail ?? "Invalid registration");
      } else {
        console.log("Registration successful:", data);
        if (data.access_token) {
          localStorage.setItem("access_token", data.access_token);
          const profileResponse = await fetchWithService("/users/me/", "BACKEND", {
            headers: {
              Authorization: `Bearer ${data.access_token}`,
            },
          });
          if (!profileResponse.ok) {
            alert("Registration succeeded but failed to fetch user info.");
            return;
          }
          const userData = await profileResponse.json();
          setUser(userData);
          navigate("/");
        } else {
          navigate("/login");
        }
      }
    } catch (error) {
      console.error("Registration error:", error);
      alert("Something went wrong. Try again later.");
    }
  }

  return (
    <form onSubmit={handleSubmit} className={styles.signUpForm}>
      <div className={styles.signUpContainer}>
        <h2 className={styles.title}>Sign Up</h2>

        <label htmlFor="username" className={styles.inputName}>
          Username:
        </label>
        <input
          id="username"
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
          className={styles.inputBar}
        />
        {errors.username && <p className={styles.error}>{errors.username}</p>}

        <label htmlFor="email" className={styles.inputName}>
          Email:
        </label>
        <input
          id="email"
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className={styles.inputBar}
        />
        {errors.email && <p className={styles.error}>{errors.email}</p>}

        <label htmlFor="password" className={styles.inputName}>
          Password:
        </label>
        <input
          id="password"
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          className={styles.inputBar}
        />
        {errors.password && <p className={styles.error}>{errors.password}</p>}

        <label htmlFor="passwordRep" className={styles.inputName}>
          Repeat Password:
        </label>
        <input
          id="passwordRep"
          type="password"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
          className={styles.inputBar}
        />
        {errors.confirmPassword && (
          <p className={styles.error}>{errors.confirmPassword}</p>
        )}

        <button type="submit" className={styles.submit}>
          Create Account
        </button>
      </div>
    </form>
  );
}
