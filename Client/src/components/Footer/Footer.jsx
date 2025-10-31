import './Footer.css'
import './FooterSocials.css'
import facebookLogo from '../../assets/Facebook.jpg'
import instagramLogo from '../../assets/Icon.png'
import twitterLogo from '../../assets/Twitter.png'

function Footer() {
  return (
    <footer className="footer">
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
            <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">
              <img src={facebookLogo} alt="Facebook" />
            </a>
            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer">
              <img src={instagramLogo} alt="Instagram" />
            </a>
            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
              <img src={twitterLogo} alt="Twitter" />
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