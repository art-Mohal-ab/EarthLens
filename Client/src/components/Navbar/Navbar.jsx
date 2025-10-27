import React from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import './Navbar.css'


const Navbar = () => {
    const location = useLocation()
    const navigate = useNavigate()

    const handleDashboard = () => {
        navigate('/dashboard')
    }

    const handleReport = () => {
        navigate('/dashboard')
    }

    const handleMyReports = () => {
        navigate('/my-reports')
    }

    const handleGreenAction = () => {
        navigate('/dashboard')
    }

    const handleProfile = () => {
        navigate('/profile')
    }

    const handleSignOut = () => {
        localStorage.removeItem('token')
        navigate('/')
    }

    const isProfilePage = location.pathname === '/profile'
    const isMyReportsPage = location.pathname === '/my-reports'
    const isAboutPage = location.pathname === '/about'

    return (
    <header className="header">
        <a href="/" className='logo'>Earth<br/>lens</a>
        <img src="/logo.png" alt="Earthlens Logo" className="logo-img" />
        <nav className='navbar'>
            {isProfilePage || isMyReportsPage ? (
                <>
                    <a onClick={handleDashboard} className="profile-nav" style={{cursor: 'pointer'}}>Dashboard</a>
                    <a onClick={handleReport} className="profile-nav" style={{cursor: 'pointer'}}>Report</a>
                    <a onClick={handleMyReports} className="profile-nav" style={{cursor: 'pointer'}}>My Reports</a>
                    <a onClick={handleGreenAction} className="profile-nav" style={{cursor: 'pointer'}}>Green Action</a>
                    <a onClick={handleProfile} className="profile-nav" style={{cursor: 'pointer'}}>Profile</a>
                    <a onClick={handleSignOut} className="profile-nav sign-out-btn" style={{cursor: 'pointer'}}>Sign out</a>
                </>
            ) : isAboutPage ? (
                <>
                    <a href="/dashboard" className="profile-nav" style={{cursor: 'pointer'}}>Features</a>
                    <a href="/about" className="profile-nav" style={{cursor: 'pointer'}}>About Us</a>
                    <a href="/" className="profile-nav" style={{cursor: 'pointer'}}>Contact Us</a>
                    <a href="/join" className="profile-nav sign-out-btn" style={{cursor: 'pointer'}}>Join Now</a>
                </>
            ) : (
                <>
                    <a href="/">Home</a>
                    <a href="/about">About</a>
                    <a href="/">Contact</a>
                    <a href="/join">Join Now</a>
                </>
            )}
        </nav>
    </header>
   )
}
 
export default Navbar