import React from "react";
import { Link } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import "./styles/About.css";

const About = () => {
  return (
    <div>
      <Navbar />
      <section className="about-page">
      <div className="about-hero">
        <h1>About EarthLens</h1>
        <p>
          EarthLens is an AI-powered platform committed to raising environmental
          awareness through satellite data, AI analysis, and community-driven
          reports for a healthier planet.
        </p>
      </div>

      <div className="mission-vision">
        <div className="about-card">
          <h2>Mission</h2>
          <p>
            We believe in the power of community and technology to drive
            positive change. EarthLens leverages data and AI to provide
            actionable insights, empowering everyone to contribute to a
            healthier planet.
          </p>
        </div>
        <div className="about-card">
          <h2>Vision</h2>
          <p>
            Our vision is a world where every individual is empowered to take
            meaningful environmental action through community and technology.
          </p>
        </div>
      </div>

      <div className="how-it-works">
        <h2>How it works</h2>
        <div className="works-section">
          <div className="work-card">
            <h3>AI-Powered Analysis</h3>
            <p>
              Using Hugging Face and OpenAI to classify reports and provide
              actionable advice.
            </p>
          </div>
          <div className="work-card">
            <h3>Community-Driven</h3>
            <p>
              Empowering citizens to report issues and take part in solving
              local environmental challenges.
            </p>
          </div>
          <div className="work-card">
            <h3>SDG 13 Aligned</h3>
            <p>
              Supporting Climate Action through technology and collective
              community engagement.
            </p>
          </div>
        </div>
      </div>
    </section>
    <Footer />
    </div>
  );
};

export default About;
