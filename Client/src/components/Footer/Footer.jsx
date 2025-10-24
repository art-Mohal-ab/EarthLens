import React from 'react'
import './Footer.css'

const Footer = () => {
    return ( <footer className="footer">
          <div className="footer-container">
        <div>
          <a href="/" className="footer-logo">EarthLens</a>
          <p className="footer-text">Seeing the world through a greener lens.</p>
        </div>

        <div>
          <h3 className="footer-heading">Quick Links</h3>
          <ul className="footer-links">
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </div>

        <div>
          <h3 className="footer-heading">Contact</h3>
          <p>Email: earthlens@gmail.com</p>
          <p>Phone: +254 700 000 000</p>
          <div className="footer-socials">
            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer">
              <img src="https://cdn-icons-png.flaticon.com/512/174/174855.png" alt="Instagram" />
            </a>
            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
              <img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" alt="Twitter" />
            </a>
            <a href="https://github.com" target="_blank" rel="noopener noreferrer">
              <img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" alt="GitHub" />
            </a>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        &copy; 2025 EarthLens. All rights reserved.
      </div>
    </footer>
    )
}

export default Footer