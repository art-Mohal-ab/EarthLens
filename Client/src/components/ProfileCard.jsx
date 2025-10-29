import React from 'react';

const ProfileCard = ({ userData, onEdit }) => {
  return (
    <div className="user-info-card">
      <div className="user-avatar">
        <div className="avatar-placeholder">
          {userData?.username ? userData.username.charAt(0).toUpperCase() : 'U'}
        </div>
      </div>
      <div className="user-details">
        <h2 className="user-name">{userData?.username || ''}</h2>
        <p className="user-email">{userData?.email || ''}</p>
        <div className="user-badge">
          <span className="badge-text">
            Joined {userData?.created_at ? new Date(userData.created_at).toLocaleDateString() : ''}
          </span>
        </div>
      </div>
      <div className="impact-score-section">
        <h3 className="score-title">Impact Score</h3>
        <div className="score-value">{userData?.impact_score || 0}</div>
      </div>
      <button className="edit-profile-btn" onClick={onEdit}>
        Edit Profile
      </button>
    </div>
  );
};

export default ProfileCard;
