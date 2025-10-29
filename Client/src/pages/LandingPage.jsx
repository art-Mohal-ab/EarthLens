import React from 'react';
import Navbar from '../components/Navbar/Navbar';
import Footer from '../components/Footer/Footer';
import Hero from '../components/Hero/Hero';
import Cards from '../components/Cards/Cards';
import IssueCards from '../components/IssueCards/IssueCards';
import '../styles/LandingPage.css';
import SupportCards from '../components/SupportCards/SupportCards';


const LandingPage = () => {
  return (
    <main className="landing-page">
      <Navbar />
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
      <SupportCards/>
      <Footer />
    </main>
  );
};

export default LandingPage;