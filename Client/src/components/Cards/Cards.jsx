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
      title: "Community Projects",
      text: "Explore ongoing green projects in your area.",
      link: "/projects",
    },
    {
      title: "Eco Tips",
      text: "Learn simple habits to help protect the planet.",
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
