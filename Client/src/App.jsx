import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";

import Navbar from "./components/Navbar/Navbar.jsx";
import Footer from "./components/Footer/Footer.jsx";
import Report from "./pages/Report.jsx";
import GreenActions from "./pages/GreenActions.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import About from "./pages/About.jsx";
import LandingPage from "./pages/LandingPage.jsx";
import Signup from "./pages/Signup.jsx";
import Login from "./pages/Login.jsx";
import MyReportspage from "./pages/MyReportspage.jsx";
import Profile from "./pages/Profile.jsx";
import Contact from "./pages/Contact.jsx";

const AppContent = () => {
  const location = useLocation();
  const showFooterPages = ["/", "/about", "/contact"];
  const shouldShowFooter = showFooterPages.includes(location.pathname);
  const hideNavbarPages = ["/dashboard", "/join", "/login"];
  const shouldShowNavbar = !hideNavbarPages.includes(location.pathname);

  return (
    <div className="app-container">
      {shouldShowNavbar && <Navbar />}
      <main className="main-content">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/report" element={<Report />} />
          <Route path="/green-actions" element={<GreenActions />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/join" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/my-reports" element={<MyReportspage />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </main>
      {shouldShowFooter && <Footer />}
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
