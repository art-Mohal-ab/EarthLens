import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import { API_BASE_URL } from "../services/api";
import "./Login.css";

const Login = () => {
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const email = e.target.email.value;
    const password = e.target.password.value;

    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      const { access_token } = response.data;
      localStorage.setItem("token", access_token);

      navigate('/dashboard');
    } catch (err) {
      console.error("Login error:", err.response?.data || err.message);
      
      let errorMessage = "Login failed";
      
      if (err.response?.data) {
        if (err.response.data.details) {
          errorMessage = Object.values(err.response.data.details).flat().join(', ');
        } else if (err.response.data.error) {
          errorMessage = err.response.data.error;
        } else if (err.response.data.message) {
          errorMessage = err.response.data.message;
        }
      } else if (err.request) {
        errorMessage = "Cannot connect to server. Please ensure the backend is running.";
      } else {
        errorMessage = err.message || "Login failed";
      }
      
      setError(errorMessage);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Welcome Back To EarthLens</h2>
        <form onSubmit={handleSubmit}>
          <label htmlFor="email">Email or Username</label>
          <input
            type="text"
            id="email"
            name="email"
            placeholder="you@example.com or username"
            required
          />

          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            placeholder="Enter your password"
            required
          />

          <button type="submit" className="login-btn">Sign In</button>
        </form>

        {error && <p className="error-message">{error}</p>}

        <p className="signup-text">
          New here? <Link to="/join" className="signup-link">Create an account</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
