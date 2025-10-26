import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar/Navbar';
import Footer from '../components/Footer/Footer';

const HomeNavbar = () => {
  return (
    <header className="header">
        <a href="/" className='logo'>Earth<br/>lens</a>
        <img src="/logo.png" alt="Earthlens Logo" className="logo-img" />
        <nav className='navbar'>
            <a href="/">Home</a>
            <a href="/">Features</a>
            <a href="/about">About Us</a>
            <a href="/">Contact Us</a>
            <a href="/">Join Now</a>
        </nav>
    </header>
  );
};

function HomePage() {
  return (
    <div>
      <HomeNavbar />
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h1>Welcome to EarthLens</h1>
        <p>Monitor environmental changes with satellite data.</p>
        <Link to="/dashboard">
          <button style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}>Go to Dashboard</button>
        </Link>
      </div>
      <Footer />
    </div>
  );
}

export default HomePage;
