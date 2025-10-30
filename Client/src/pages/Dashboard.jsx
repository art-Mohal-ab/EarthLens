import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ReportList from "../components/ReportList";
import FilterBar from "../components/FilterBar";
import EditReportModal from "../components/EditReportModal";
import ViewReportModal from "../components/ViewReportModal";
import "../styles/Dashboard.css";
import "../styles/ViewReportModal.css";

function Dashboard() {
  const navigate = useNavigate();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({});
  const [selectedReport, setSelectedReport] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [viewReport, setViewReport] = useState(null);

  useEffect(() => {
    window.scrollTo(0, 0);
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
    setTimeout(() => {
      window.scrollTo(0, 0);
    }, 100);
    fetchReports();
  }, [filters]);

  const fetchReports = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/login");
        return;
      }

      const queryParams = new URLSearchParams();
      if (filters.location) queryParams.append('location', filters.location);
      if (filters.category) queryParams.append('category', filters.category);
      if (filters.dateFrom) queryParams.append('date_from', filters.dateFrom);
      if (filters.dateTo) queryParams.append('date_to', filters.dateTo);

      const response = await fetch(`http://localhost:5003/api/reports?${queryParams}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setReports(data.reports || []);
      } else {
        setReports([]);
      }
    } catch (err) {
      console.error('Error fetching reports:', err);
      if (err.response?.status === 401) {
        localStorage.removeItem("token");
        navigate("/login");
      } else {
        setError('Failed to load reports');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };



  const handleViewDetails = (reportId) => {
    const report = reports.find(r => r.id === reportId);
    setViewReport(report);
    setIsViewModalOpen(true);
  };

  const handleEditReport = (report) => {
    setSelectedReport(report);
    setIsModalOpen(true);
  };

  const handleDeleteReport = (reportId) => {
    setReports(prev => prev.filter(r => r.id !== reportId));
  };

  const handleSaveReport = async (reportId, updatedData) => {
    console.log('Saving report:', reportId, updatedData);
    setReports(prev => prev.map(r => r.id === reportId ? { ...r, ...updatedData } : r));
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedReport(null);
  };

  const handleCloseViewModal = () => {
    setIsViewModalOpen(false);
    setViewReport(null);
  };

  const handleDashboard = () => {
    navigate("/dashboard");
  };

  const handleReport = () => {
    navigate("/report");
  };

  const handleMyReports = () => {
    navigate("/my-reports");
  };

  const handleGreenAction = () => {
    navigate("/green-actions");
  };

  const handleProfile = () => {
    navigate("/profile");
  };

  const handleSignOut = () => {
    localStorage.removeItem('token');
    navigate("/");
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="logo">EARTHLENS</div>
        <button onClick={handleDashboard} className="sidebar-btn">Dashboard</button>
        <button onClick={handleReport} className="sidebar-btn">Report</button>
        <button onClick={handleMyReports} className="sidebar-btn">My Reports</button>
        <button onClick={handleGreenAction} className="sidebar-btn">Green Action</button>
        <button onClick={handleProfile} className="sidebar-btn">Profile</button>
        <button onClick={handleSignOut} className="sign-out-btn">Sign out</button>
      </aside>

      <main className="main">
        <h1>Recent Reports</h1>
        <FilterBar
          filters={filters}
          onFilterChange={handleFilterChange}
        />
        <ReportList
          reports={reports}
          onViewDetails={handleViewDetails}
          onEditReport={handleEditReport}
          onDeleteReport={handleDeleteReport}
          loading={loading}
          error={error}
          showEditDelete={false}
        />
      </main>

      <EditReportModal
        report={selectedReport}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSave={handleSaveReport}
      />

      <ViewReportModal
        key={viewReport?.id}
        report={viewReport}
        isOpen={isViewModalOpen}
        onClose={handleCloseViewModal}
      />
    </div>
  );
}

export default Dashboard;
