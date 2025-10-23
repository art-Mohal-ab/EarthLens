import React from 'react';
import './styles/About.css';

const About = () => {
  return (
    <div className="earhlens-container">
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">About Earhlens</h1>
          <p className="hero-subtitle">
            An AI-powered monitor designed to raise environmental awareness and
            promote sustainable practices.
          </p>
        </div>
      </section>

      <section className="mission-section">
        <div className="container">
          <div className="mission-content">
            <div className="mission-card">
              <h2 className="mission-heading">Our Mission</h2>
              <p className="mission-text">
                We believe in the power of community and technology to drive positive change.
                Earhlens leverages advanced AI to analyze user-submitted reports, providing
                valuable insights into environmental challenges and recommending effective
                solutions. Our platform is designed to be accessible, informative, and
                actionable, enabling everyone to contribute to a healthier planet.
              </p>
            </div>
            <div className="vision-card">
              <h2 className="vision-heading">Our Vision</h2>
              <p className="vision-text">
                Our vision is to create a world where every individual is empowered to take meaningful environmental action.
                Through the fusion of community collaboration and intelligent technology, EarthLens envisions a future where awareness leads to action, and collective efforts drive lasting positive change for our planet.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="how-it-works-section">
        <div className="container">
          <h2 className="section-title">How It Works</h2>
          <div className="cards-grid">
            <div className="feature-card">
              <h3 className="card-title">AI-Powered Analysis</h3>
              <ul className="card-list">
                <li>Using Hugging Face and OpenAI to classify environmental issues</li>
                <li>Providing actionable advice and recommendations</li>
              </ul>
            </div>

            <div className="feature-card">
              <h3 className="card-title">Community Engagement</h3>
              <ul className="card-list">
                <li>Empowering citizens to report and discuss local environmental challenges</li>
                <li>Facilitating collective action and community collaboration</li>
              </ul>
            </div>

            <div className="feature-card">
              <h3 className="card-title">SDG 13 Aligned</h3>
              <p className="card-text">
                Support Climate Action through technology, awareness, and community engagement.
              </p>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
};

export default About;
