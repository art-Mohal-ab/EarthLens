import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';

function HomePage() {
  return (
    <div>
      <Navbar />
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
