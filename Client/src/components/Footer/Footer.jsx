import React from 'react'
import './Footer.css'


const Footer = () => {
    return ( <footer className="footer">
          <div className="footer-container">
        <div>
          <h2 className="footer-logo">EarthLens</h2>
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
            <img src="/assets/facebook.png" alt="Facebook" />
            <img src="/assets/insta.png" alt="Instagram" />
            <img src="/assets/twitter.png" alt="Twitter" />
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