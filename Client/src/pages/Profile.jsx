import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar/Navbar';
import ProfileCard from '../components/ProfileCard';
import SavedItemsList from '../components/SavedItemsList';
import api from '../services/api';
import '../styles/Profile.css';

const Profile = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [savedItems, setSavedItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Mock data for profile
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

      const mockSavedItems = [
        {
          id: 1,
          title: "Illegal Dumping Near River",
          description: "Large amounts of plastic waste dumped near the riverbank affecting water quality and wildlife.",
          location: "Nairobi, Kenya",
          created_at: "2025-10-10T00:00:00Z",
          image_url: "/RIVER.png"
        }
      ];

      setUserData(mockUserData);
      setSavedItems(mockSavedItems);
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

  const handleRemoveSavedItem = async (itemId) => {
    try {
      // Mock removal - just update local state
      setSavedItems(savedItems.filter(item => item.id !== itemId));
    } catch (err) {
      console.error('Error removing saved item:', err);
      alert('Failed to remove saved item');
    }
  };

  const handleHome = () => {
    navigate("/");
  };

  const handleDashboard = () => {
    navigate("/dashboard");
  };

  const handleReport = () => {
    navigate("/dashboard"); // Assuming report functionality is under dashboard
  };

  const handleMyReports = () => {
    navigate("/my-reports");
  };

  const handleGreenAction = () => {
    navigate("/dashboard"); // Placeholder, adjust if route exists
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

                {/* Saved Items */}
                <SavedItemsList
                  savedItems={savedItems}
                  onRemoveItem={handleRemoveSavedItem}
                  loading={false}
                  error={null}
                />
              </>
            )}

            {activeTab === 'edit' && (
              <div className="edit-profile-section">
                <h2>Edit Profile</h2>
                <p>Profile editing functionality coming soon...</p>
              </div>
            )}

            {activeTab === 'security' && (
              <div className="security-section">
                <h2>Security Settings</h2>
                <p>Security settings functionality coming soon...</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Profile;
