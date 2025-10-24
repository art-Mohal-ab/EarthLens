import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div style={{ textAlign: 'center', padding: '50px' }}>
      <h1>Welcome to EarthLens</h1>
      <p>Monitor environmental changes with satellite data.</p>
      <Link to="/dashboard">
        <button style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}>Go to Dashboard</button>
      </Link>
    </div>
  );
}

export default HomePage;
