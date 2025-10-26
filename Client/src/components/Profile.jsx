
import React, { useState, useEffect } from 'react';
import '../styles/Profile.css';

const Profile = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setUserData({
        name: "Karani Lau",
        email: "karanilau@gmail.com",
        joinDate: "October 2025",
        impactScore: 12,
        reportsSubmitted: 12,
        commentsMade: 16,
        topCategory: "Pollution",
        recentActivities: [
          { type: "report", text: "Submitted report on plastic waste", time: "3 days ago" },
          { type: "comment", text: "Commented on deforestation report", time: "7 days ago" }
        ]
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="profile-container">
      {/* Header */}
      <div className="profile-header">
        <h1 className="profile-title">Profile</h1>
      </div>

      <div className="profile-content">
        {/* Left Column */}
        <div className="profile-left">
          {/* User Info Card */}
          <div className="user-info-card">
            <div className="user-avatar">
              <div className="avatar-placeholder">KL</div>
            </div>
            <div className="user-details">
              <h2 className="user-name">{userData.name}</h2>
              <p className="user-email">{userData.email}</p>
              <div className="user-badge">
                <span className="badge-text">Joined {userData.joinDate}</span>
              </div>
            </div>
            <div className="impact-score-section">
              <h3 className="score-title">Impact Score</h3>
              <div className="score-value">{userData.impactScore}</div>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="profile-right">
          {/* Overview Section */}
          <div className="overview-section">
            <div className="overview-actions">
              <button className="action-btn active">Overview</button>
              <button className="action-btn">Edit Profile</button>
              <button className="action-btn">Security</button>
            </div>
          </div>
          {/* Activity Summary */}
          <div className="activity-summary-card">
            <h2 className="section-subtitle">Activity Summary</h2>
            <p className="summary-description">Your environmental impact and contributions</p>

            <div className="stats-container">
              <div className="stat-item">
                <div className="stat-number">{userData.reportsSubmitted}</div>
                <div className="stat-label">Reports Submitted</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">{userData.commentsMade}</div>
                <div className="stat-label">Comments Made</div>
              </div>
            </div>

            <div className="top-category-card">
              <h4 className="category-title">{userData.topCategory}</h4>
              <p className="category-subtitle">Top Category</p>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="recent-activity-card">
            <h2 className="section-subtitle">Recent Activity</h2>

            <div className="activity-list">
              {userData.recentActivities.map((activity, index) => (
                <div key={index} className="activity-item">
                  <div className="activity-content">
                    <p className="activity-text">{activity.text}</p>
                    <span className="activity-time">{activity.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>


        </div>
      </div>
    </div>
  );
};

export default Profile;
