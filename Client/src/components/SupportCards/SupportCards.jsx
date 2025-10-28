import React from 'react';
import './SupportCards.css'; 

const SupportCards = () => {
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

  return (
    <section className="support-section">
      <div className="cards-container">
        {cards.map((card, index) => (
          <div key={index} className="support-card">
            <h3>{card.title}</h3>
            <p>{card.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default SupportCards;
