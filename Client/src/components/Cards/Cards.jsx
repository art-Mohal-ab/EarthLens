import React from "react";
import { Link } from "react-router-dom";
import "./Cards.css";

const Cards = () => {
  const cardData = [
    {
      title: "Illegal Dumping",
      text: "Report unauthorized waste disposal and keep our environment clean.",
      link: "/report",
    },
    {
      title: "Air Pollution",
      text: "Identify areas suffering from industrial or traffic pollution.",
      link: "/projects",
    },
    {
      title: "Deforestation",
      text: "Help track forest loss and report areas needing replanting.",
      link: "/eco-tips",
    },
  ];

  return (
    <section className="cards-section">
      <div className="cards-container">
        {cardData.map((card, index) => (
          <Link key={index} to={card.link} className="card">
            <h3>{card.title}</h3>
            <p>{card.text}</p>
          </Link>
        ))}
      </div>
    </section>
  );
};

export default Cards;
