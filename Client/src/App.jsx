import React from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";
import Footer from "./components/Footer/Footer";
import Login from "./pages/Login";
import LandingPage from './pages/LandingPage';
import Signup from "./pages/Signup";
import Dashboard from "./Dashboard";
import HomePage from "./HomePage";
import About from "./About";

const AppContent = () => {
  const location = useLocation();
  const hideNavFooter = ['/login', '/join'].includes(location.pathname);

  return (
    <div className="app">
      {!hideNavFooter && <Navbar />}
      <main>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/join" element={<Signup />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
      {!hideNavFooter && <Footer />}
    </div>
  );
};

const App = () => {
  return (
    <Router>
      <AppContent />
    </Router>
  );
};

export default App;
