import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { API_BASE_URL } from "../services/api";
import "../styles/Report.css";

const ReportForm = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);
  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };
  const handleDragLeave = () => setDragging(false);
  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    setFile(e.dataTransfer.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    const formData = new FormData();
    formData.append("title", e.target.title.value);
    formData.append("description", e.target.description.value);
    formData.append("location", e.target.location.value);
    if (file) {
      formData.append("image", file);
    }

    try {
      const response = await api.post("/reports", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      alert("Report submitted successfully!");
      navigate("/my-reports");
    } catch (err) {
      console.error("Error submitting report:", err);
      if (err.response?.status === 401) {
        localStorage.removeItem("token");
        navigate("/login");
      } else {
        setError("Failed to submit report. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Environmental Issue Report</h1>
        <p className="subtitle">
          Help us track environmental challenges by submitting a report below.
        </p>
      </header>

      <form className="report-form" onSubmit={handleSubmit}>
        <h2 className="section-title">Report Details</h2>

        <div className="form-group">
          <label htmlFor="title">Title of the Report</label>
          <input
            type="text"
            id="title"
            name="title"
            placeholder="e.g., Illegal dumping in the river"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            placeholder="Describe the issue clearly..."
            required
          ></textarea>
        </div>

        <div className="form-group">
          <label htmlFor="location">Location</label>
          <input
            type="text"
            id="location"
            name="location"
            placeholder="e.g., Nairobi River, near Globe Roundabout"
            required
          />
        </div>

        <div className="form-group">
          <label>Upload Evidence (optional)</label>
          <div
            className={`upload-area ${dragging ? "dragging" : ""} ${
              file ? "has-file" : ""
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <p className="upload-text">
              {file ? file.name : "Drag & drop a file or click to upload"}
            </p>
            <p className="upload-hint">Supported formats: JPG, PNG, PDF</p>
            <input
              type="file"
              id="fileInput"
              style={{ display: "none" }}
              onChange={handleFileChange}
            />
            <label htmlFor="fileInput" className="upload-btn">
              Browse File
            </label>
          </div>
        </div>

        {error && <p className="error-message">{error}</p>}
        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? "Submitting..." : "Submit Report"}
        </button>
      </form>

      <footer>
        © {new Date().getFullYear()} EarthLens | Environmental Reporting Platform
      </footer>
    </div>
  );
};

export default ReportForm;
