import React from 'react'
import './Footer.css'

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <a href="/">Contact</a>
                <a href="/">About</a>
                <a href="/">Quick Links</a>
            </div>

            <p className="footer-copy">
                © {new Date().getFullYear()} EarthLens. All rights reserved.
            </p>
        </footer>
    )
}

export default Footer