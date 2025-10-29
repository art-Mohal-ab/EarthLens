import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import "./Signup.css";

const Signup = () => {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [username, setUsername] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const username = e.target.username.value;
    const email = e.target.email.value;
    const password = e.target.password.value;

    try {
      const response = await api.post("/auth/register", {
        username,
        email,
        password,
      });

      const { access_token } = response.data;
      localStorage.setItem("token", access_token);

      navigate('/dashboard');
    } catch (err) {
      console.error("Signup error:", err.response?.data);
      const errorMessage = err.response?.data?.details
        ? Object.values(err.response.data.details).flat().join(', ')
        : err.response?.data?.error || "Signup failed";
      setError(errorMessage);
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-box">
        <h2>
          Your journey starts here
          <br />
          Take the first step
        </h2>

        <form onSubmit={handleSubmit}>
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            placeholder="Enter your username (letters, numbers, underscores only)"
            value={username}
            onChange={(e) => setUsername(e.target.value.replace(/[^a-zA-Z0-9_]/g, ''))}
            required
          />

          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            placeholder="you@example.com"
            required
          />

          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            placeholder="Enter your password (min 8 chars, uppercase, lowercase, number)"
            required
          />

          <button type="submit" className="signup-btn">
            Sign Up
          </button>
        </form>

        {error && <p className="error-message">{error}</p>}

        <p className="signin-text">
          Already have an account?{" "}
          <Link to="/login" className="signin-link">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;
