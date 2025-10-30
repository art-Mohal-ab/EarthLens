import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const location = useLocation();

  const authenticatedPages = [
    "/dashboard",
    "/report",
    "/my-reports",
    "/green-actions",
    "/profile",
  ];

  const token = localStorage.getItem("token");
  const isAuthenticated = !!token;
  const isAuthenticatedPage = authenticatedPages.includes(location.pathname);

  const handleSignOut = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  if (isAuthenticated && isAuthenticatedPage) {
    return (
      <header className="header">
        <Link to="/" className="logo">
          Earth
          <br />
          lens
        </Link>
        <img src="/logo.png" alt="Earthlens Logo" className="logo-img" />
        <nav className="navbar">
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/report">Report</Link>
          <Link to="/my-reports">My Reports</Link>
          <Link to="/green-actions">Green Actions</Link>
          <Link to="/profile">Profile</Link>
          <button onClick={handleSignOut} className="sign-out-btn">
            Sign Out
          </button>
        </nav>
      </header>
    );
  }

  return (
    <header className="header">
      <Link to="/" className="logo">
        Earth
        <br />
        lens
      </Link>
      <img src="/logo.png" alt="Earthlens Logo" className="logo-img" />
      <nav className="navbar">
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">Contact</Link>
        <Link to="/login">Join Now</Link>
      </nav>
    </header>
  );
};

export default Navbar;
