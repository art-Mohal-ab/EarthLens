import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import LandingPage from './pages/LandingPage';
import Signup from "./pages/Signup";
import Login from './pages/Login'; 
import Contact from './pages/Contact';

const noFooterRoutes = ["/login"];

const AppContent = () => {
  const location = useLocation();
  const hideNavFooter = ['/login', '/join', '/signup', '/dashboard'].includes(location.pathname);

  return (
    <div>
      {!hideNavFooter && <Navbar />}
      <main>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/Signup" element={<Signup />} />
            <Route path="/Contact" element={<Contact />}/>

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
