import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";
import Hero from "./components/Hero/Hero";
import Cards from "./components/Cards/Cards";
import IssueCards from "./components/IssueCards/IssueCards";
import Footer from "./components/Footer/Footer";
import Login from "./pages/Login";
import LandingPage from './pages/LandingPage';
import Signup from "./pages/Signup";
import Contact from "./pages/Contact";


const noFooterRoutes = ["/login"];

const App = () => {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <main>
        <main>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/Signup" element={<Signup />} />
             <Route path="/contact" element={<Contact />} />
          </Routes>
        </main>
        </main>
        <Footer />
      </div>
    </Router>
  );
};


export default App;
