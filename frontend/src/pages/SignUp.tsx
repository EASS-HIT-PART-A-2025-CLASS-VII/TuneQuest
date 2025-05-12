import styles from "./SignUp.module.css";
import { useState } from "react";

export default function SignUp() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
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
        <h2>Sign Up</h2>
        <label htmlFor="username">Username:{""}</label>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <label htmlFor="email">Email:{""}</label>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <label htmlFor="password">Password:{""}</label>
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <label htmlFor="passwordRep">Repeat Password:{""}</label>
        <input
          type="password"
          name="confirmPassword"
          placeholder="Repeat Password"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
        <button type="submit">Create Account</button>
      </div>
    </form>
  );
}
