import React from "react"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Dashboard from "./pages/Dashboard.jsx"
import HomePage from "./pages/HomePage.jsx"
import About from "./pages/About.jsx"
import LandingPage from "./pages/LandingPage.jsx"
import Signup from "./pages/Signup.jsx"
import Login from "./pages/Login.jsx"
import MyReportspage from "./pages/MyReportspage.jsx"
import Profile from "./pages/Profile.jsx"

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/about" element={<About />} />
        <Route path="/join" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/my-reports" element={<MyReportspage />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Router>
  );
};

export default App;
