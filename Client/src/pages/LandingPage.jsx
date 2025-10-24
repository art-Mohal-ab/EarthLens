import React from 'react';
import Hero from '../components/Hero/Hero';
import Cards from '../components/Cards/Cards';
import IssueCards from '../components/IssueCards/IssueCards';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <main className="landing-page">
      <Hero />
      <Cards />
      <IssueCards />
      <section className="hero hero2">
        <div className="hero-content">
          <h1>Together, We Build Climate Resilience</h1>
        </div>
      </section>
    </main>
  );
};

export default LandingPage;