import React from 'react'
import './Navbar.css'


const Navbar = () => {
    return ( 
    <header className="header">
        <a href="/" className='logo'>Earth<br/>lens</a>
        <img src="/logo.png" alt="Earthlens Logo" className="logo-img" />
        <nav className='navbar'>
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/">Contact</a>
            <a href="/join">Join Now</a>
        </nav>
    </header>
   )
}
 
export default Navbar