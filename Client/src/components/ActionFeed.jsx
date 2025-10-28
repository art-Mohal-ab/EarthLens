import React from 'react';
import './ActionFeed.css';

const ActionFeed = ({ actions, loading, completedActions, onMarkDone }) => {
  if (loading) {
    return <div className="loading">Loading green actions...</div>;
  }

  if (!actions || !actions.length) {
    return <div className="no-actions">No actions found for this category.</div>;
  }

  return (
    <div className="action-feed">
      {actions.map((action, index) => (
        <div key={index} className="action-card">
          <h3>{action.title}</h3>
          <div className="tags">
            <button className="tag category">{action.category}</button>
            <button className="tag difficulty">{action.difficulty}</button>
          </div>
          <p className="description">{action.description}</p>
          <p className="benefit">{action.impact}</p>
          <button 
            className={`mark-done ${completedActions?.has(action.title) ? 'completed' : ''}`}
            onClick={() => onMarkDone?.(action.title)}
          >
            {completedActions?.has(action.title) ? 'Completed ✓' : 'Mark Done'}
          </button>
        </div>
      ))}
    </div>
  );
};

export default ActionFeed;