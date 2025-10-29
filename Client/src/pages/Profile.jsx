import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar/Navbar';
import ProfileCard from '../components/ProfileCard';
import api from '../services/api';
import '../styles/Profile.css';

const Profile = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    window.scrollTo(0, 0);
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
    setTimeout(() => {
      window.scrollTo(0, 0);
    }, 100);
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      setLoading(true);
      setError(null);

      const mockUserData = {
        username: "Karani Lau",
        email: "karanilau@gmail.com",
        created_at: "2025-10-01T00:00:00Z",
        impact_score: 12,
        reports_submitted: 12,
        comments_made: 16,
        top_category: "Pollution",
        recent_activities: [
          { type: "report", text: "Submitted report on plastic waste", time: "3 days ago" },
          { type: "comment", text: "Commented on deforestation report", time: "7 days ago" }
        ]
      };

      setUserData(mockUserData);
    } catch (err) {
      console.error('Error fetching profile:', err);
      setError('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const handleEditProfile = () => {
    setActiveTab('edit');
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const updatedData = {
      username: formData.get('username'),
      email: formData.get('email'),
    };

    try {
      setUserData(prev => ({ ...prev, ...updatedData }));
      setActiveTab('overview');
    } catch (error) {
      console.error('Error updating profile:', error);
      alert('Failed to update profile. Please try again.');
    }
  };

  const handleUpdatePassword = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const currentPassword = formData.get('currentPassword');
    const newPassword = formData.get('newPassword');
    const confirmPassword = formData.get('confirmPassword');

    if (newPassword !== confirmPassword) {
      alert('New passwords do not match.');
      return;
    }

    try {
      alert('Password updated successfully!');
      e.target.reset();
    } catch (error) {
      console.error('Error updating password:', error);
      alert('Failed to update password. Please try again.');
    }
  };



  const handleHome = () => {
    navigate("/");
  };

  const handleDashboard = () => {
    navigate("/dashboard");
  };

  const handleReport = () => {
    navigate("/dashboard");
  };

  const handleMyReports = () => {
    navigate("/my-reports");
  };

  const handleGreenAction = () => {
    navigate("/dashboard");
  };

  const handleProfile = () => {
    navigate("/profile");
  };

  const handleSignOut = () => {
    localStorage.removeItem('token');
    navigate("/");
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="profile-container">
      <Navbar />
      <main className="main" style={{ width: '100%', marginLeft: 0 }}>
        <h1>Profile</h1>

        <div className="profile-content">
          {/* Left Column */}
          <div className="profile-left">
            <ProfileCard userData={userData} onEdit={handleEditProfile} />
          </div>

          {/* Right Column */}
          <div className="profile-right">
            {/* Overview Section */}
            <div className="overview-section">
              <div className="overview-actions">
                <button
                  className={`action-btn ${activeTab === 'overview' ? 'active' : ''}`}
                  onClick={() => setActiveTab('overview')}
                >
                  Overview
                </button>
                <button
                  className={`action-btn ${activeTab === 'edit' ? 'active' : ''}`}
                  onClick={() => setActiveTab('edit')}
                >
                  Edit Profile
                </button>
                <button
                  className={`action-btn ${activeTab === 'security' ? 'active' : ''}`}
                  onClick={() => setActiveTab('security')}
                >
                  Security
                </button>
              </div>
            </div>

            {activeTab === 'overview' && (
              <>
                {/* Activity Summary */}
                <div className="activity-summary-card">
                  <h2 className="section-subtitle">Activity Summary</h2>
                  <p className="summary-description">Your environmental impact and contributions</p>

                  <div className="stats-container">
                    <div className="stat-item">
                      <div className="stat-number">{userData?.reports_submitted || 0}</div>
                      <div className="stat-label">Reports Submitted</div>
                    </div>
                    <div className="stat-item">
                      <div className="stat-number">{userData?.comments_made || 0}</div>
                      <div className="stat-label">Comments Made</div>
                    </div>
                  </div>
                </div>

                {/* Recent Activity */}
                <div className="recent-activity-card">
                  <h2 className="section-subtitle">Recent Activity</h2>

                  <div className="activity-list">
                    <div className="activity-item">
                      <div className="activity-content">
                        <p className="activity-text">{userData?.top_category || 'No category'}</p>
                        <span className="activity-time">Top Category</span>
                      </div>
                    </div>
                    {userData?.recent_activities?.map((activity, index) => (
                      <div key={index} className="activity-item">
                        <div className="activity-content">
                          <p className="activity-text">{activity.text}</p>
                          <span className="activity-time">{activity.time}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>


              </>
            )}

            {activeTab === 'edit' && (
              <div className="edit-profile-section">
                <h2>Edit Profile</h2>
                <form className="edit-profile-form" onSubmit={handleSaveProfile}>
                  <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input
                      type="text"
                      id="username"
                      name="username"
                      defaultValue={userData?.username || ''}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      defaultValue={userData?.email || ''}
                      required
                    />
                  </div>
                  <div className="form-actions">
                    <button type="button" className="cancel-btn" onClick={() => setActiveTab('overview')}>Cancel</button>
                    <button type="submit" className="save-btn">Save Changes</button>
                  </div>
                </form>
              </div>
            )}

            {activeTab === 'security' && (
              <div className="security-section">
                <h2>Security Settings</h2>
                <form className="security-form" onSubmit={handleUpdatePassword}>
                  <div className="form-group">
                    <label htmlFor="current-password">Current Password</label>
                    <input
                      type="password"
                      id="current-password"
                      name="currentPassword"
                      placeholder="Enter current password"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="new-password">New Password</label>
                    <input
                      type="password"
                      id="new-password"
                      name="newPassword"
                      placeholder="Enter new password"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="confirm-password">Confirm New Password</label>
                    <input
                      type="password"
                      id="confirm-password"
                      name="confirmPassword"
                      placeholder="Confirm new password"
                      required
                    />
                  </div>
                  <div className="form-actions">
                    <button type="submit" className="save-btn">Update Password</button>
                  </div>
                </form>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Profile;
