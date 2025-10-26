import React from 'react';
import ReportCard from './ReportCard';

const ReportList = ({ reports, onViewDetails, loading, error }) => {
  if (loading) {
    return <div className="loading">Loading reports...</div>;
  }

  if (error) {
    return <div className="error">Error loading reports: {error}</div>;
  }

  if (!reports || reports.length === 0) {
    return <div className="no-reports">No reports found.</div>;
  }

  return (
    <section className="cards">
      {reports.map((report) => (
        <ReportCard
          key={report.id}
          report={report}
          onViewDetails={onViewDetails}
        />
      ))}
    </section>
  );
};

export default ReportList;
