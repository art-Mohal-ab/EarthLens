import React from 'react'
import { Link } from 'react-router-dom'
import './Navbar.css'


const Navbar = () => {
    return (
    <header className="header">
        <Link to="/" className='logo'>Earth<br/>lens</Link>
        <img src="/logo.png" alt="Earthlens Logo" className="logo-img" />
        <nav className='navbar'>
            <Link to="/">Home</Link>
            <Link to="/About">About</Link>
            <Link to="/Contact">Contact</Link>
            <Link to="/login">Join Now</Link>
        </nav>
    </header>
   )
}
 
export default Navbar