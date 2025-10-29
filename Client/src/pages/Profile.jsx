import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ProfileCard from "../components/ProfileCard";
import api from "../services/api";
import "../styles/Profile.css";

const Profile = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("overview");

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

      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/login");
        return;
      }

      const response = await api.get("/profile", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const profileData = response.data.profile;

      // Transform the data to match the expected format
      const transformedData = {
        username: profileData.username,
        email: profileData.email,
        created_at: profileData.created_at,
        impact_score: profileData.impact.reports_submitted + profileData.impact.comments_made,
        reports_submitted: profileData.impact.reports_submitted,
        comments_made: profileData.impact.comments_made,
        top_category: profileData.top_category,
        recent_activities: [
          ...profileData.recent_activity.reports.map(report => ({
            type: "report",
            text: `Submitted report: ${report.title}`,
            time: new Date(report.created_at).toLocaleDateString(),
          })),
          ...profileData.recent_activity.comments.map(comment => ({
            type: "comment",
            text: `Commented: ${comment.content}`,
            time: new Date(comment.created_at).toLocaleDateString(),
          })),
        ].slice(0, 5), // Limit to 5 recent activities
      };

      setUserData(transformedData);
    } catch (err) {
      console.error("Error fetching profile:", err);
      if (err.response?.status === 401) {
        localStorage.removeItem("token");
        navigate("/login");
      } else {
        setError("Failed to load profile");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleEditProfile = () => {
    setActiveTab("edit");
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const updatedData = {
      username: formData.get("username"),
      email: formData.get("email"),
    };

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/login");
        return;
      }

      const response = await api.put("/auth/me", updatedData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      // Update local state with the response data
      const updatedUser = response.data.user;
      setUserData((prev) => ({
        ...prev,
        username: updatedUser.username,
        email: updatedUser.email,
      }));
      setActiveTab("overview");
      alert("Profile updated successfully!");
    } catch (error) {
      console.error("Error updating profile:", error);
      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        navigate("/login");
      } else if (error.response?.data?.error) {
        alert(error.response.data.error);
      } else if (error.response?.data?.details) {
      
        const details = error.response.data.details;
        const errorMessages = Object.entries(details).map(([field, messages]) =>
          `${field}: ${messages.join(', ')}`
        ).join('\n');
        alert(`Validation failed:\n${errorMessages}`);
      } else {
        alert("Failed to update profile. Please try again.");
      }
    }
  };

  const handleUpdatePassword = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const currentPassword = formData.get("currentPassword");
    const newPassword = formData.get("newPassword");
    const confirmPassword = formData.get("confirmPassword");

    if (newPassword !== confirmPassword) {
      alert("New passwords do not match.");
      return;
    }

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/login");
        return;
      }

      await api.put("/auth/me", {
        current_password: currentPassword,
        new_password: newPassword,
      }, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      alert("Password updated successfully!");
      e.target.reset();
    } catch (error) {
      console.error("Error updating password:", error);
      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        navigate("/login");
      } else {
        alert("Failed to update password. Please try again.");
      }
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
    localStorage.removeItem("token");
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
      <main className="main" style={{ width: "100%", marginLeft: 0 }}>
        <h1>Profile</h1>

        <div className="profile-content">
          <div className="profile-left">
            <ProfileCard userData={userData} onEdit={handleEditProfile} />
          </div>

          <div className="profile-right">
            <div className="overview-section">
              <div className="overview-actions">
                <button
                  className={`action-btn ${
                    activeTab === "overview" ? "active" : ""
                  }`}
                  onClick={() => setActiveTab("overview")}
                >
                  Overview
                </button>
                <button
                  className={`action-btn ${
                    activeTab === "edit" ? "active" : ""
                  }`}
                  onClick={() => setActiveTab("edit")}
                >
                  Edit Profile
                </button>
                <button
                  className={`action-btn ${
                    activeTab === "security" ? "active" : ""
                  }`}
                  onClick={() => setActiveTab("security")}
                >
                  Security
                </button>
              </div>
            </div>

            {activeTab === "overview" && (
              <>
                <div className="activity-summary-card">
                  <h2 className="section-subtitle">Activity Summary</h2>
                  <p className="summary-description">
                    Your environmental impact and contributions
                  </p>

                  <div className="stats-container">
                    <div className="stat-item">
                      <div className="stat-number">
                        {userData?.reports_submitted || 0}
                      </div>
                      <div className="stat-label">Reports Submitted</div>
                    </div>
                    <div className="stat-item">
                      <div className="stat-number">
                        {userData?.comments_made || 0}
                      </div>
                      <div className="stat-label">Comments Made</div>
                    </div>
                  </div>
                </div>

                <div className="recent-activity-card">
                  <h2 className="section-subtitle">Recent Activity</h2>

                  <div className="activity-list">
                    <div className="activity-item">
                      <div className="activity-content">
                        <p className="activity-text">
                          {userData?.top_category || "No category"}
                        </p>
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

            {activeTab === "edit" && (
              <div className="edit-profile-section">
                <h2>Edit Profile</h2>
                <form
                  className="edit-profile-form"
                  onSubmit={handleSaveProfile}
                >
                  <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input
                      type="text"
                      id="username"
                      name="username"
                      defaultValue={userData?.username || ""}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      defaultValue={userData?.email || ""}
                      required
                    />
                  </div>
                  <div className="form-actions">
                    <button
                      type="button"
                      className="cancel-btn"
                      onClick={() => setActiveTab("overview")}
                    >
                      Cancel
                    </button>
                    <button type="submit" className="save-btn">
                      Save Changes
                    </button>
                  </div>
                </form>
              </div>
            )}

            {activeTab === "security" && (
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
                    <label htmlFor="confirm-password">
                      Confirm New Password
                    </label>
                    <input
                      type="password"
                      id="confirm-password"
                      name="confirmPassword"
                      placeholder="Confirm new password"
                      required
                    />
                  </div>
                  <div className="form-actions">
                    <button type="submit" className="save-btn">
                      Update Password
                    </button>
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
