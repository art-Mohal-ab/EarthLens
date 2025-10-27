import React from "react"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Navbar from "./components/Navbar/Navbar"
import Footer from "./components/Footer/Footer"
import Report from "./pages/Report.jsx"
import GreenActions from "./pages/GreenActions.jsx"

const App = () => {
  return(
    <Router>
      <div>
        <Navbar/>
        <Routes>
          <Route path="/" element={<Report/>} />
          <Route path="/report" element={<Report/>} />
          <Route path="/green-actions" element={<GreenActions/>} />
        </Routes>
        <Footer/>
      </div>
    </Router>
  )
}

export default App