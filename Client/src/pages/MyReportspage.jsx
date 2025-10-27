import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar/Navbar';
import MyReportList from '../components/MyReportList';
import EditReportModal from '../components/EditReportModal';
import api from '../services/api';
import '../styles/MyReportpage.css';

const ReportsPage = () => {
  const navigate = useNavigate();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingReport, setEditingReport] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);

  useEffect(() => {
    fetchUserReports();
  }, []);

  const fetchUserReports = async () => {
    try {
      setLoading(true);
      setError(null);

      const mockUserReports = [
        {
          id: 1,
          title: "Plastic Waste Accumulation",
          description: "Large amount of plastic bottles and bags accumulating near the shopping center.",
          location: "Kandoba Farm, Kenya",
          ai_category: "Waste Management",
          ai_advice: "Contact county waste management. Organize community cleanup. Advocate for recycling bins.",
          created_at: "2025-10-10T00:00:00Z",
          image_url: "assets/RIVER.png",
          user_id: 1
        },
        {
          id: 2,
          title: "Air Pollution from Factory",
          description: "Visible smoke emissions from nearby factory affecting air quality in residential area.",
          location: "Uranus, Kenya",
          ai_category: "Air Pollution",
          ai_advice: "Report to NEAA. Document emission times. Gather community signatures for petition.",
          created_at: "2025-10-14T00:00:00Z",
          image_url: "assets/AIR.png",
          user_id: 1
        },
        {
          id: 4,
          title: "Illegal Poaching of Animals",
          description: "Poaching harms wildlife, disrupts ecosystems, and endangers species survival.",
          location: "Nairobi, Kenya",
          ai_category: "Poaching",
          ai_advice: "Contact wildlife authorities. Report to local police. Document evidence with photos.",
          created_at: "2025-10-10T00:00:00Z",
          image_url: "assets/ANIMAL.png",
          user_id: 1
        }
      ];

      setReports(mockUserReports);
    } catch (err) {
      console.error('Error fetching reports:', err);
      setError('Failed to load reports');
    } finally {
      setLoading(false);
    }
  };

  const getCurrentUserId = () => {
    return 1;
  };

  const handleEditReport = (report) => {
    setEditingReport(report);
    setShowEditModal(true);
  };

  const handleSaveReport = async (reportId, formData) => {
    try {

      setReports(reports.map(report =>
        report.id === reportId ? { ...report, ...formData } : report
      ));
    } catch (err) {
      throw err;
    }
  };

  const handleDeleteReport = async (reportId) => {
    if (window.confirm('Are you sure you want to delete this report?')) {
      try {
        setReports(reports.filter(report => report.id !== reportId));
      } catch (err) {
        console.error('Error deleting report:', err);
        alert('Failed to delete report');
      }
    }
  };
  const handleViewDetails = (reportId) => {
    navigate(`/report/${reportId}`);
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

  return (
    <div className="reports-page">
      <Navbar />
      <main className="main" style={{ width: '100%', marginLeft: 0 }}>
        <h1>My Reports</h1>
        <MyReportList
          reports={reports}
          onEditReport={handleEditReport}
          onDeleteReport={handleDeleteReport}
          onViewDetails={handleViewDetails}
          loading={loading}
          error={error}
        />
      </main>

      <EditReportModal
        report={editingReport}
        isOpen={showEditModal}
        onClose={() => setShowEditModal(false)}
        onSave={handleSaveReport}
      />
    </div>
  );
};

export default ReportsPage;
