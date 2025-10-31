import React from 'react';
import { useNavigate } from 'react-router-dom';
import './SupportCards.css'; 

const SupportCards = () => {
  const navigate = useNavigate();

  const cards = [
    {
      title: 'Join as Agent',
      description: 'Become a climate resilience champion in your community',
    },
    {
      title: 'Partner With Us',
      description: 'Collaborate to scale our impact across regions',
    },
    {
      title: 'Support Our Mission',
      description: 'Help us take care of our planet',
    },
  ];

  const handleCardClick = () => {
    navigate('/contact');
  };

  return (
    <section className="support-section">
      <div className="cards-container">
        {cards.map((card, index) => (
          <div 
            key={index} 
            className="support-card clickable-card" 
            onClick={handleCardClick}
            role="button"
            tabIndex={0}
            onKeyPress={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                handleCardClick();
              }
            }}
          >
            <h3>{card.title}</h3>
            <p>{card.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default SupportCards;
