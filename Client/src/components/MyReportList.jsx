import React from 'react';

const MyReportList = ({ reports, onEditReport, onDeleteReport, onViewDetails, loading, error, showEditDelete = false }) => {
  if (loading) {
    return <div className="loading">Loading your reports...</div>;
  }

  if (error) {
    return <div className="error">Error loading reports: {error}</div>;
  }

  if (!reports || reports.length === 0) {
    return <div className="no-reports">You haven't submitted any reports yet.</div>;
  }

  return (
    <section className="cards">
      {reports.map((report) => (
        <article key={report.id} className="card">
          <div className="image-section">
            <img src={report.image_url || '/placeholder.png'} alt={report.title} />
          </div>
          <div className="text-section">
            <h3>{report.title}</h3>
            <div className="metadata-buttons">
              <button className="meta-btn">{report.ai_category || 'Uncategorized'}</button>
              <button className="meta-btn">{report.location}</button>
              <button className="meta-btn">{new Date(report.created_at).toLocaleDateString()}</button>
              <button className="meta-btn">Reported by {report.reporter || 'Anonymous'}</button>
            </div>
            <p>{report.description}</p>
            {showEditDelete && report.ai_advice && (
              <div className="ai-recommendations">
                <strong>AI Recommendations:</strong> {report.ai_advice}
              </div>
            )}
            <div className="ai-action-buttons">
              <button className="edit-btn" onClick={() => onEditReport(report)}>Edit</button>
              <button className="delete-btn" onClick={() => onDeleteReport(report.id)}>Delete</button>
            </div>
          </div>
        </article>
      ))}
    </section>
  );
};

export default MyReportList;
