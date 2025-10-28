import React from "react"
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom"
import Footer from "./components/Footer/Footer"
import Report from "./pages/Report.jsx"
import GreenActions from "./pages/GreenActions.jsx"
import Dashboard from "./pages/Dashboard.jsx"
import About from "./pages/About.jsx"
import LandingPage from "./pages/LandingPage.jsx"
import Signup from "./pages/Signup.jsx"
import Login from "./pages/Login.jsx"
import MyReportspage from "./pages/MyReportspage.jsx"
import Profile from "./pages/Profile.jsx"

const AppContent = () => {
  const location = useLocation();
  const hideFooter = location.pathname === '/green-actions' || location.pathname === '/report';

  return (
    <div>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/report" element={<Report/>} />
        <Route path="/green-actions" element={<GreenActions/>} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/about" element={<About />} />
        <Route path="/join" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/my-reports" element={<MyReportspage />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
      {!hideFooter && <Footer/>}
    </div>
  );
};

const App = () => {
  return(
    <Router>
      <AppContent />
    </Router>
  )
}

export default App
