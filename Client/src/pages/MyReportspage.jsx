import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import MyReportList from "../components/MyReportList";
import EditReportModal from "../components/EditReportModal";
import api from "../services/api";
import "../styles/MyReportpage.css";

const ReportsPage = () => {
  const navigate = useNavigate();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingReport, setEditingReport] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);

  const [currentPage, setCurrentPage] = useState(1);
  const reportsPerPage = 2;

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
          description:
            "Large amount of plastic bottles and bags accumulating near the shopping center.",
          location: "Kandoba Farm, Kenya",
          ai_category: "Waste Management",
          ai_advice:
            "Contact county waste management. Organize community cleanup. Advocate for recycling bins.",
          created_at: "2025-10-10T00:00:00Z",
          image_url: "/assets/plastic.png",
        },
        {
          id: 2,
          title: "Air Pollution from Factory",
          description:
            "Visible smoke emissions from nearby factory affecting air quality in residential area.",
          location: "Uranus, Kenya",
          ai_category: "Air Pollution",
          ai_advice:
            "Report to NEAA. Document emission times. Gather community signatures for petition.",
          created_at: "2025-10-14T00:00:00Z",
          image_url: "/assets/Air.png",
        },
        {
          id: 3,
          title: "Illegal Poaching of Animals",
          description:
            "Poaching harms wildlife, disrupts ecosystems, and endangers species survival.",
          location: "Nairobi, Kenya",
          ai_category: "Poaching",
          ai_advice:
            "Contact wildlife authorities. Report to local police. Document evidence with photos.",
          created_at: "2025-10-10T00:00:00Z",
          image_url: "/assets/Poaching.png",
        },
        {
          id: 4,
          title: "Deforestation in Local Forest",
          description:
            "Tree cutting observed near the hill forest area for charcoal burning.",
          location: "Murang’a, Kenya",
          ai_category: "Deforestation",
          ai_advice:
            "Alert forest services. Mobilize community patrols. Replant trees.",
          created_at: "2025-10-18T00:00:00Z",
          image_url: "/assets/deforestation.png",
        },
      ];

      setReports(mockUserReports);
    } catch (err) {
      console.error("Error fetching reports:", err);
      setError("Failed to load reports");
    } finally {
      setLoading(false);
    }
  };

  const handleEditReport = (report) => {
    setEditingReport(report);
    setShowEditModal(true);
  };

  const handleSaveReport = (reportId, formData) => {
    setReports((prevReports) =>
      prevReports.map((r) => (r.id === reportId ? { ...r, ...formData } : r))
    );
  };

  const handleDeleteReport = (reportId) => {
    if (window.confirm("Are you sure you want to delete this report?")) {
      setReports((prevReports) => prevReports.filter((r) => r.id !== reportId));
    }
  };

  const handleViewDetails = (reportId) => {
    navigate(`/report/${reportId}`);
  };

  const indexOfLastReport = currentPage * reportsPerPage;
  const indexOfFirstReport = indexOfLastReport - reportsPerPage;
  const currentReports = reports.slice(indexOfFirstReport, indexOfLastReport);
  const totalPages = Math.ceil(reports.length / reportsPerPage);

  const handleNextPage = () => {
    if (currentPage < totalPages) setCurrentPage(currentPage + 1);
  };

  const handlePrevPage = () => {
    if (currentPage > 1) setCurrentPage(currentPage - 1);
  };

  return (
    <div className="reports-page">
      <main className="main">
        <h2>My Reports</h2>

        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p className="error">{error}</p>
        ) : (
          <>
            <MyReportList
              reports={currentReports}
              onEdit={handleEditReport}
              onDelete={handleDeleteReport}
              onView={handleViewDetails}
            />

            <div className="pagination">
              <button
                onClick={handlePrevPage}
                disabled={currentPage === 1}
                className="page-btn"
              >
                ◀ Prev
              </button>

              <span className="page-info">
                Page {currentPage} of {totalPages}
              </span>

              <button
                onClick={handleNextPage}
                disabled={currentPage === totalPages}
                className="page-btn"
              >
                Next ▶
              </button>
            </div>
          </>
        )}
      </main>

      {showEditModal && (
        <EditReportModal
          report={editingReport}
          onSave={handleSaveReport}
          onClose={() => setShowEditModal(false)}
        />
      )}
    </div>
  );
};

export default ReportsPage;
