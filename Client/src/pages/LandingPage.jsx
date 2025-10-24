import React from 'react';
import Hero from '../components/Hero/Hero';
import Cards from '../components/Cards/Cards';
import IssueCards from '../components/IssueCards/IssueCards';
import './LandingPage.css';
import SupportCards from '../components/SupportCards/SupportCards';

const LandingPage = () => {
  return (
    <div>
      <Hero />
      <Cards />
      <IssueCards />
      
      <section className="hero hero2">
        <div className="hero-content">
          <h1>Together, We Build Climate Resilience</h1>
        </div>
      </section>
      <SupportCards />
    </div>
  );
};

export default LandingPage;