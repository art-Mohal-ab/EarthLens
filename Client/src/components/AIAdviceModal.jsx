import React from 'react';
import './AIAdviceModal.css';

const AIAdviceModal = ({ isOpen, onClose, category, advice }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>AI Analysis Complete</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        
        <div className="modal-body">
          <div className="category-section">
            <h3>Issue Category</h3>
            <span className="category-tag">{category}</span>
          </div>
          
          <div className="advice-section">
            <h3>Recommended Actions</h3>
            <p>{advice}</p>
          </div>
        </div>
        
        <div className="modal-footer">
          <button className="ok-btn" onClick={onClose}>Got it!</button>
        </div>
      </div>
    </div>
  );
};

export default AIAdviceModal;