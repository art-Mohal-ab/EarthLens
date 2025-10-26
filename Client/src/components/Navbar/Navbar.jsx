import React from 'react'
import { useNavigate } from 'react-router-dom';
import './Navbar.css'


const Navbar = () => {
    const navigate = useNavigate();

    const handleDashboard = () => {
        navigate("/dashboard");
    };

    const handleReport = () => {
        navigate("/dashboard"); // Assuming report functionality is under dashboard
    };

    const handleMyReports = () => {
        navigate("/my-reports");
    };

    const handleGreenAction = () => {
        navigate("/dashboard"); // Placeholder, adjust if route exists
    };

    const handleProfile = () => {
        navigate("/profile");
    };

    const handleSignOut = () => {
        localStorage.removeItem('token');
        navigate("/");
    };

    return (
    <header className="header">
        <a href="/" className='logo'>Earth<br/>lens</a>
        <img src="/logo.png" alt="Earthlens Logo" className="logo-img" />
        <nav className='navbar'>
            <button className="nav-button" onClick={handleDashboard}>Dashboard</button>
            <button className="nav-button" onClick={handleReport}>Report</button>
            <button className="nav-button" onClick={handleMyReports}>My Reports</button>
            <button className="nav-button" onClick={handleGreenAction}>Green Action</button>
            <button className="nav-button" onClick={handleProfile}>Profile</button>
            <button className="nav-button sign-out-button" onClick={handleSignOut}>Sign out</button>
        </nav>
    </header>
   )
}
 
export default Navbar