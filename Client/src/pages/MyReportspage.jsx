import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/MyReportpage.css';

const ReportsPage = () => {
  const navigate = useNavigate();

  const handleHome = () => {
    navigate("/");
  };

  const handleDashboard = () => {
    navigate("/dashboard");
  };

  const handleReport = () => {
    navigate("/dashboard"); // Assuming report functionality is under dashboard
  };

  const handleMyReports = () => {
    navigate("/my-reports");
  };

  const handleGreenAction = () => {
    navigate("/dashboard"); // Placeholder, adjust if route exists
  };

  const handleProfile = () => {
    navigate("/profile");
  };

  const handleSignOut = () => {
    navigate("/");
  };

  const reports = [
    {
      id: 1,
      title: "Plastic Waste Accumulation",
      category: "Waste Management",
      location: "Kandoba Farm, Kenya",
      date: "10/10/2025",
      description: "",
      reporter: "Sarah Mwangi",
      image: "/RIVER.png",
      recommendations: [
        "Large amount of plastic bottles and bags accumulating near the shopping center.",
        "Contact county waste management.",
        "Organize community cleanup.",
        "Advocate for recycling bins."
      ]
    },
    {
      id: 2,
      title: "Air Pollution from Factory",
      category: "Air Pollution",
      location: "Uranus, Kenya",
      date: "10/14/2025",
      description: "",
      reporter: "John Ouma",
      image: "/AIR.png",
      recommendations: [
        "Visible smoke emissions from nearby factory affecting air quality in residential area.",
        "Report to NEAA.",
        "Document emission times.",
        "Gather community signatures for petition."
      ]
    },

    {
      id: 4,
      title: "Illegal Poaching of Animals",
      category: "Poaching",
      location: "Nairobi, Kenya",
      date: "10/10/2025",
      description: "",
      reporter: "Mary Akinyi",
      image: "/ANIMAL.png",
      recommendations: [
        "Poaching harms wildlife, disrupts ecosystems, and endangers species survival.",
        "Contact wildlife authorities.",
        "Report to local police.",
        "Document evidence with photos."
      ]
    }
  ];

  return (
    <div className="reports-page">
      <aside className="sidebar">
        <div className="logo">EARTHLENS</div>
        <button onClick={handleHome}>Home</button>
        <button onClick={handleDashboard}>Dashboard</button>
        <button onClick={handleReport}>Report</button>
        <button onClick={handleMyReports}>My Reports</button>
        <button onClick={handleGreenAction}>Green Action</button>
        <button onClick={handleProfile}>Profile</button>
        <button onClick={handleSignOut}>Sign out</button>
      </aside>
      <main className="main">
        <h1>My Reports</h1>
        <section className="cards">
          {reports.map((report) => (
            <article key={report.id} className="card">
              <div className="image-section">
                <img src={report.image} alt={report.title} />
              </div>
              <div className="text-section">
                <h3>{report.title}</h3>
                <div className="metadata-buttons">
                  <button className="meta-btn">{report.category}</button>
                  <button className="meta-btn">{report.location}</button>
                  <button className="meta-btn">{report.date}</button>
                  <button className="meta-btn">Reported by {report.reporter}</button>
                </div>
                <p>{report.description}</p>
                {report.recommendations && report.recommendations.length > 0 && (
                  <div className="ai-recommendations">
                    <strong>AI Recommendations:</strong> {report.recommendations.join(', ')}
                  </div>
                )}
                <a className="details" href="#">View details →</a>
              </div>
            </article>
          ))}
        </section>
      </main>
    </div>
  );
};

export default ReportsPage;
