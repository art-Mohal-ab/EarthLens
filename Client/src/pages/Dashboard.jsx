import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ReportList from "../components/ReportList";
import FilterBar from "../components/FilterBar";
import "../styles/Dashboard.css";

function Dashboard() {
  const navigate = useNavigate();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({});

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
          user: { username: "Sarah Mwangi" }
        },
        {
          id: 2,
          title: "Air Pollution from Factory",
          description: "Visible smoke emissions from nearby factory affecting air quality in residential area.",
          location: "Kisumu, Kenya",
          ai_category: "Air Pollution",
          created_at: "2025-10-14T00:00:00Z",
          image_url: "/assets/AIR.png",
          user: { username: "John Ouma" }
        },
        {
          id: 3,
          title: "Flooding in Residential Area",
          description: "Poor drainage causing severe flooding during rainy season affecting multiple homes.",
          location: "Mombasa, Kenya",
          ai_category: "Flooding",
          created_at: "2025-10-13T00:00:00Z",
          image_url: "/assets/4.png",
          user: { username: "Grace Kimani" }
        },
        {
          id: 4,
          title: "Illegal Poaching of Animals",
          description: "Poaching harms wildlife, disrupts ecosystems, and endangers species survival.",
          location: "Nairobi, Kenya",
          ai_category: "Poaching",
          created_at: "2025-10-10T00:00:00Z",
          image_url: "/assets/ANIMAL.png",
          user: { username: "Mary Akinyi" }
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
    navigate(`/report/${reportId}`);
  };

  const handleHome = () => {
    navigate("/");
  };

  const handleMyReports = () => {
    navigate("/my-reports");
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
        <button onClick={handleHome}>Home</button>
        <button>Dashboard</button>
        <button>Report</button>
        <button onClick={handleMyReports}>My Reports</button>
        <button>Green Action</button>
        <button onClick={handleProfile}>Profile</button>
        <button onClick={handleSignOut}>Sign out</button>
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
          loading={loading}
          error={error}
        />
      </main>
    </div>
  );
}

export default Dashboard;
