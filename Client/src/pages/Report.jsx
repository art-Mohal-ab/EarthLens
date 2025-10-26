import React, { useState } from 'react';
import '../styles/Report.css';

const Report = () => {
  const [formData, setFormData] = useState({
    summary: '',
    description: '',
    location: '',
    file: null
  });

  const [isDragging, setIsDragging] = useState(false);

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [id]: value
    }));
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData(prev => ({
        ...prev,
        file
      }));
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      setFormData(prev => ({
        ...prev,
        file
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!formData.summary || !formData.description || !formData.location) {
      alert('Please fill in all required fields.');
      return;
    }

    console.log('Form submitted:', formData);
    alert('Thank you for your report! Your submission helps protect our environment.');

    setFormData({
      summary: '',
      description: '',
      location: '',
      file: null
    });
  };

  const triggerFileInput = () => {
    document.getElementById('fileInput').click();
  };

  return (
    <div className="container">
      <header>
        <h1>Report Environmental Issues</h1>
        <p className="subtitle">
          Empower your community by reporting environmental issues. Your narrative helps raise
          awareness and drive action for a healthier planet.
        </p>
      </header>

      <main>
        <form className="report-form" onSubmit={handleSubmit}>
          <div className="form-section">
            <h2 className="section-title">Report Details</h2>

            <div className="form-group">
              <label htmlFor="summary">A concise summary of the issue</label>
              <input
                type="text"
                id="summary"
                value={formData.summary}
                onChange={handleInputChange}
                placeholder="Briefly describe the environmental issue"
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">
                Elaborate on the environmental issue, its impact, and what you observed
              </label>
              <textarea
                id="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Provide detailed information about the issue, its effects, and your observations"
              />
            </div>

            <div className="form-group">
              <label htmlFor="location">
                Where did this happen? (e.g., specific location, landmark)
              </label>
              <input
                type="text"
                id="location"
                value={formData.location}
                onChange={handleInputChange}
                placeholder="Enter the location where you observed the issue"
              />
            </div>
          </div>

          <div className="form-section">
            <h2 className="section-title">Add Evidence</h2>

            <div className="form-group">
              <div
                className={`upload-area ${isDragging ? 'dragging' : ''} ${formData.file ? 'has-file' : ''}`}
                onClick={triggerFileInput}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <div className="upload-text">
                  {formData.file
                    ? `File selected: ${formData.file.name}`
                    : 'Upload photo evidence'
                  }
                </div>
                <div className="upload-hint">Click to browse or drag images here</div>
                <button type="button" className="upload-btn">Upload Media</button>
                <input
                  type="file"
                  id="fileInput"
                  onChange={handleFileSelect}
                  accept="image/*"
                  style={{ display: 'none' }}
                />
              </div>
            </div>
          </div>

          <button type="submit" className="submit-btn">
            Submit Report
          </button>
        </form>
      </main>

      <footer>
        <p>Together we can make a difference for our planet</p>
      </footer>
    </div>
  );
};

export default Report;