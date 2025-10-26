import React from 'react';

const SavedItemsList = ({ savedItems, onRemoveItem, loading, error }) => {
  if (loading) {
    return <div className="loading">Loading saved items...</div>;
  }

  if (error) {
    return <div className="error">Error loading saved items: {error}</div>;
  }

  if (!savedItems || savedItems.length === 0) {
    return <div className="no-saved-items">No saved items yet.</div>;
  }

  return (
    <div className="saved-items-list">
      <h3>Saved Reports</h3>
      <div className="saved-items-grid">
        {savedItems.map((item) => (
          <div key={item.id} className="saved-item-card">
            <div className="saved-item-image">
              <img src={item.image_url || '/placeholder.png'} alt={item.title} />
            </div>
            <div className="saved-item-content">
              <h4>{item.title}</h4>
              <p className="saved-item-meta">
                {item.location} • {new Date(item.created_at).toLocaleDateString()}
              </p>
              <p className="saved-item-description">{item.description}</p>
              <div className="saved-item-actions">
                <button className="view-btn" onClick={() => window.open(`/report/${item.id}`, '_blank')}>
                  View
                </button>
                <button className="remove-btn" onClick={() => onRemoveItem(item.id)}>
                  Remove
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SavedItemsList;
