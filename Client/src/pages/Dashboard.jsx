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
    fetchReports();
  }, [filters]);

  const fetchReports = async () => {
    try {
      setLoading(true);
      setError(null);

      const mockReports = [
        {
          id: 1,
          title: "Illegal Dumping Near River",
          description: "Large amounts of plastic waste dumped near the riverbank affecting water quality and wildlife.",
          location: "Nairobi, Kenya",
          ai_category: "Waste Management",
          created_at: "2025-10-10T00:00:00Z",
          image_url: "/assets/RIVER.png",
          user: { username: "Sarah Mwangi" },
          ai_advice: "Contact county waste management. Organize community cleanup. Advocate for recycling bins."
        },
        {
          id: 2,
          title: "Air Pollution from Factory",
          description: "Visible smoke emissions from nearby factory affecting air quality in residential area.",
          location: "Kisumu, Kenya",
          ai_category: "Air Pollution",
          created_at: "2025-10-14T00:00:00Z",
          image_url: "/assets/AIR.png",
          user: { username: "John Ouma" },
          ai_advice: "Report to NEAA. Document emission times. Gather community signatures for petition."
        },
        {
          id: 3,
          title: "Flooding in Residential Area",
          description: "Poor drainage causing severe flooding during rainy season affecting multiple homes.",
          location: "Mombasa, Kenya",
          ai_category: "Flooding",
          created_at: "2025-10-13T00:00:00Z",
          image_url: "/assets/4.png",
          user: { username: "Grace Kimani" },
          ai_advice: "Contact local authorities. Document flood patterns. Join community drainage improvement initiatives."
        },
        {
          id: 4,
          title: "Illegal Poaching of Animals",
          description: "Poaching harms wildlife, disrupts ecosystems, and endangers species survival.",
          location: "Nairobi, Kenya",
          ai_category: "Poaching",
          created_at: "2025-10-10T00:00:00Z",
          image_url: "/assets/ANIMAL.png",
          user: { username: "Mary Akinyi" },
          ai_advice: "Contact wildlife authorities. Report to local police. Document evidence with photos."
        }
      ];

      let filteredReports = mockReports;
      if (filters.location) {
        filteredReports = filteredReports.filter(report =>
          report.location.toLowerCase().includes(filters.location.toLowerCase())
        );
      }
      if (filters.category) {
        filteredReports = filteredReports.filter(report =>
          report.ai_category === filters.category
        );
      }
      if (filters.dateFrom) {
        filteredReports = filteredReports.filter(report =>
          new Date(report.created_at) >= new Date(filters.dateFrom)
        );
      }
      if (filters.dateTo) {
        filteredReports = filteredReports.filter(report =>
          new Date(report.created_at) <= new Date(filters.dateTo)
        );
      }

      setReports(filteredReports);
    } catch (err) {
      console.error('Error fetching reports:', err);
      setError('Failed to load reports');
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
