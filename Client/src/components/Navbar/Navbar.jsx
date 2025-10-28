import React from 'react'
import './Navbar.css'


const Navbar = () => {
    return ( 
    <header className="header">
        <Link to="/" className='logo'>Earth<br/>lens</Link>
        <img src="/logo.png" alt="Earthlens Logo" className="logo-img" />
        <nav className='navbar'>
            <a href="/">Home</a>
            <a href="/">Features</a>
            <a href="/about">About Us</a>
            <a href="/">Contact Us</a>
            <a href="/">Join Now</a>
        </nav>
    </header>
   )
}
 
export default Navbar