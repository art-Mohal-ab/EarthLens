// Cards.jsx
import React from "react";
import "./CardStyles.css";

const cards = [
  { title: "Report Issues", body: "Report unauthorized waste disposal and keep our environment clean." },
  { title: "Gain Insights", body: "Identify areas suffering from industrial or traffic pollution." },
  { title: "Take Action", body: "Help track forest loss and report areas needing replanting." }
];

export default function Cards() {
  return (
    <section className="cards-grid">
      {cards.map((c) => (
        <article key={c.title} className="report-card" role="article" aria-label={c.title}>
          <h3 className="card-title">{c.title}</h3>
          <p className="card-body">{c.body}</p>
        </article>
      ))}
    </section>
  );
}
