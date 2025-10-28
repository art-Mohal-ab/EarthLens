import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Signup.css";

const Signup = () => {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulate signup success and redirect to dashboard
    navigate('/dashboard');
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
            placeholder="Enter your username"
            required
          />

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

          <button type="submit" className="signup-btn">
            Sign Up
          </button>
        </form>

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
