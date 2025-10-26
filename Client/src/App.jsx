import React from "react"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import HomePage from "./pages/HomePage"
import About from "./About"
import Profile from "./pages/Profile"
import MyReportspage from "./pages/MyReportspage"

const App = () => {
  return(
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/about" element={<About />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/my-reports" element={<MyReportspage />} />
      </Routes>
    </Router>
  )
}

export default App
