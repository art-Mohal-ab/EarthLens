import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";
import Hero from "./components/Hero/Hero";
import Cards from "./components/Cards/Cards";
import IssueCards from "./components/IssueCards/IssueCards";
import Footer from "./components/Footer/Footer";
import Login from "./pages/Login";

const App = () => {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <main>
          <Routes>
            <Route 
              path="/" 
              element={
                <>
                  <Hero />
                  <Cards />
                  <IssueCards />
                </>
              } 
            />
            <Route path="/login" element={<Login />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
