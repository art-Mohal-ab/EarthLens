import React from "react";
import "./IssueCards.css";

import wasteImg from "../../assets/plastic.png";
import pollutionImg from "../../assets/Industry.png";
import treesImg from "../../assets/forest.png";

const IssueCards = () => {
  const issues = [
    {
      title: "Illegal Dumping",
      text: "Report unauthorized waste disposal and keep our environment clean.",
      img: wasteImg,
    },
    {
      title: "Air Pollution",
      text: "Identify areas suffering from industrial or traffic pollution.",
      img: pollutionImg,
    },
    {
      title: "Deforestation",
      text: "Help track forest loss and report areas needing replanting.",
      img: treesImg,
    },
  ];

  return (
    <section className="issuecards-section">
      <h2 className="issuecards-title"></h2>
      <div className="issuecards-container">
        {issues.map((issue, index) => (
          <div key={index} className="issue-card">
            <img src={issue.img} alt={issue.title} className="issue-img" />
            <h3>{issue.title}</h3>
            <p>{issue.text}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default IssueCards;
