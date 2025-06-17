import styles from "./Login.module.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "@/contexts/UserContext";
import { fetchWithService } from "@/utils/api";

export default function Login() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const navigate = useNavigate();
  const { setUser } = useUser();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetchWithService('/users/login/', 'BACKEND', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      if (!response.ok) {
        alert("Invalid username or password");
        return;
      }

      localStorage.setItem("access_token", data.access_token);
      const profileResponse = await fetchWithService("/users/me/", 'BACKEND', {
        headers: {
          Authorization: `Bearer ${data.access_token}`,
        },
      });
      if (!profileResponse.ok) {
        alert("Login succeeded but failed to fetch user info.");
        return;
      }
      const userData = await profileResponse.json();
      setUser(userData);
      navigate("/");
    } catch (error) {
      console.error("Login error:", error);
      alert("Something went wrong. Try again later.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.loginForm}>
      <div className={styles.loginContainer}>
        <h2 className={styles.title}>Log In</h2>

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

        <button type="submit" className={styles.submit}>
          Log In
        </button>
      </div>
    </form>
  );
}
