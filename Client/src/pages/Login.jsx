import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Login.css";

const Login = () => {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Welcome Back To EarthLens</h2>
        <form onSubmit={handleSubmit}>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            placeholder="you@example.com"
            required
          />

          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            placeholder="Enter your password"
            required
          />

          <button type="submit" className="login-btn">Sign In</button>
        </form>

        <p className="signup-text">
          New here? <Link to="/join" className="signup-link">Create an account</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
