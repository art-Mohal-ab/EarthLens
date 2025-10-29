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

      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/login");
        return;
      }

      const response = await api.get("/reports/my-reports", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setReports(response.data.reports || []);
    } catch (err) {
      console.error("Error fetching reports:", err);
      if (err.response?.status === 401) {
        localStorage.removeItem("token");
        navigate("/login");
      } else {
        setError("Failed to load reports");
      }
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
              onEditReport={handleEditReport}
              onDeleteReport={handleDeleteReport}
              onViewDetails={handleViewDetails}
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
          isOpen={showEditModal}
          onSave={handleSaveReport}
          onClose={() => setShowEditModal(false)}
        />
      )}
    </div>
  );
};

export default ReportsPage;
