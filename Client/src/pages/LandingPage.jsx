import React from 'react';
import Navbar from '../components/Navbar/Navbar';  
import Hero from '../components/Hero/Hero';
import Cards from '../components/Cards/Cards';
import IssueCards from '../components/IssueCards/IssueCards';
import SupportCards from '../components/SupportCards/SupportCards';
import Footer from '../components/Footer/Footer'; 
import '../styles/LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page-wrapper">
      <Navbar /> 
      <main className="landing-page">
        <Hero />
        <section className="how-earthlens-works">
          <h2>How EarthLens Works</h2>
          <Cards />
          <IssueCards />
        </section>
        <section className="hero hero2">
          <div className="hero-content">
            <h1>Together, We Build Climate Resilience</h1>
          </div>
        </section>
        <SupportCards />
      </main>
      <Footer /> 
    </div>
  );
};

export default LandingPage;
