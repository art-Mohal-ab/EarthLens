import React from 'react';
import '../styles/Dashboard.css';

const ReportCard = ({ report, onViewDetails, onEditReport, onDeleteReport, showEditDelete = false }) => {
  return (
    <article className="card">
      <div className="image-section">
        <img src={report.image_url || '/placeholder.png'} alt={report.title} />
      </div>
      <div className="text-section">
        <h3>{report.title}</h3>
        <div className="metadata-buttons">
          <button className="meta-btn">{report.ai_category || 'Uncategorized'}</button>
          <button className="meta-btn">{report.location}</button>
          <button className="meta-btn">{new Date(report.created_at).toLocaleDateString()}</button>
        </div>
        <p>{report.description}</p>
        <p className="reporter">Reported by {report.user?.username || 'Anonymous'}</p>
        {showEditDelete && report.ai_advice && (
          <div className="ai-recommendations">
            <strong>AI Recommendations:</strong> {report.ai_advice}
          </div>
        )}
        {showEditDelete && report.ai_advice && (
          <div className="ai-action-buttons">
            <button className="edit-btn" onClick={() => onEditReport(report)}>Edit</button>
            <button className="delete-btn" onClick={() => onDeleteReport(report.id)}>Delete</button>
          </div>
        )}
        <div className="action-buttons">
          <button className="details-btn" onClick={() => onViewDetails(report.id)}>View details →</button>
        </div>
      </div>
    </article>
  );
};

export default ReportCard;
