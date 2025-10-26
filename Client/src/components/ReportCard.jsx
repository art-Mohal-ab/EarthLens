import React from 'react';
import '../styles/Dashboard.css';

const ReportCard = ({ report, onViewDetails }) => {
  return (
    <article className="card">
      <div className="image-section">
        <img src={report.image_url || '/placeholder.png'} alt={report.title} />
      </div>
      <div className="text-section">
        <h3>{report.title}</h3>
        <p>
          <span className="info-box">{report.ai_category || 'Uncategorized'}</span>
          <span className="info-box">{report.location}</span>
          <span className="info-box">{new Date(report.created_at).toLocaleDateString()}</span><br />
          {report.description}<br />
          Reported by {report.user?.username || 'Anonymous'}
        </p>
        <a className="details" href="#" onClick={(e) => { e.preventDefault(); onViewDetails(report.id); }}>
          View details →
        </a>
      </div>
    </article>
  );
};

export default ReportCard;
