import React from 'react';
import './ActionFeed.css';

const ActionFeed = ({ actions, loading }) => {
  if (loading) {
    return <div className="loading">Loading green actions...</div>;
  }

  if (!actions.length) {
    return <div className="no-actions">No actions found for this category.</div>;
  }

  return (
    <div className="action-feed">
      {actions.map((action, index) => (
        <div key={index} className="action-card">
          <div className="action-header">
            <h3>{action.title}</h3>
            <span className={`difficulty ${action.difficulty?.toLowerCase()}`}>
              {action.difficulty}
            </span>
          </div>
          
          <p className="action-description">{action.description}</p>
          
          <div className="action-footer">
            <span className={`impact ${action.impact?.toLowerCase()}`}>
              Impact: {action.impact}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ActionFeed;