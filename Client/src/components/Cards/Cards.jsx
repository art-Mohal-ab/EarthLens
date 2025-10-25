import React from "react";
import { FaTrash, FaCloud, FaTree } from "react-icons/fa";
import "./Cards.css";

const Cards = () => {
  const cardData = [
    {
      title: "Illegal Dumping",
      text: "Report unauthorized waste disposal and keep our environment clean.",
      link: "/report",
      icon: <FaTrash />,
      className: "card-report",
    },
    {
      title: "Air Pollution",
      text: "Identify areas suffering from industrial or traffic pollution.",
      link: "/projects",
      icon: <FaCloud />,
      className: "card-insight",
    },
    {
      title: "Deforestation",
      text: "Help track forest loss and report areas needing replanting.",
      link: "/eco-tips",
      icon: <FaTree />,
      className: "card-action",
    },
  ];

  return (
    <section className="cards-section">
      <div className="cards-container">
        {cardData.map((card, index) => (
          <a key={index} href={card.link} className={`card ${card.className}`}>
            <div className="card-icon">{card.icon}</div>
            <h3>{card.title}</h3>
            <p>{card.text}</p>
          </a>
        ))}
      </div>
    </section>
  );
};

export default Cards;
