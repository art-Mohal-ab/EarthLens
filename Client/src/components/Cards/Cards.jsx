import React from "react";
import "./Cards.css";

const Cards = () => {
  const cardData = [
    {
      title: "Report Issue",
      text: "Capture and report environmental issues around you.",
      link: "/report",
    },
    {
      title: "Gain Insight",
      text: "Receive AI-generated insights and understand the impact of reported issues.",
      link: "/projects",
    },
    {
      title: "Take action",
      text: "Get personalized recommendations for actions you can take to address environmental challenges.",
      link: "/eco-tips",
    },
  ];

  return (
    <section className="cards-section">
      <div className="cards-container">
        {cardData.map((card, index) => (
          <a key={index} href={card.link} className="card">
            <h3>{card.title}</h3>
            <p>{card.text}</p>
          </a>
        ))}
      </div>
    </section>
  );
};

export default Cards;