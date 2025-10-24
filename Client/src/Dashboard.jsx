// Dashboard.jsx
import React from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

function Dashboard() {
  const navigate = useNavigate();

  const handleSignOut = () => {
    navigate("/");
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="logo">EARTHLENS</div>
        <button>Dashboard</button>
        <button>Report</button>
        <button>My Reports</button>
        <button>Green Action</button>
        <button>Profile</button>
        <button onClick={handleSignOut}>Sign out</button>
      </aside>

      <main className="main">
        <h1>Recent Reports</h1>
        <section className="cards">
          <article className="card">
            <div className="image-section">
              <img src="/RIVER.png" alt="Illegal Dumping Near River" />
            </div>
            <div className="text-section">
              <h3>Illegal Dumping Near River</h3>
              <p>
                <span className="info-box">Waste Management</span> <span className="info-box">Nairobi, Kenya</span> <span className="info-box">10/10/2025</span><br />
                Large amounts of plastic waste dumped near the riverbank affecting water quality and wildlife.<br />
                Reported by Sarah Mwangi
              </p>
              <a className="details" href="#">View details →</a>
            </div>
          </article>



          <article className="card">
            <div className="image-section">
              <img src="/AIR.png" alt="Air Pollution from Factory" />
            </div>
            <div className="text-section">
              <h3>Air Pollution from Factory</h3>
              <p>
                <span className="info-box">Air Pollution</span> <span className="info-box">Kisumu, Kenya</span> <span className="info-box">10/14/2025</span><br />
                Visible smoke emissions from nearby factory affecting air quality in residential area.<br />
                Reported by John Ouma
              </p>
              <a className="details" href="#">View details →</a>
            </div>
          </article>

          <article className="card">
            <div className="image-section">
              <img src="/4.png" alt="Flooding in Residential Area" />
            </div>
            <div className="text-section">
              <h3>Flooding in Residential Area</h3>
              <p>
                <span className="info-box">Flooding</span> <span className="info-box">Mombasa, Kenya</span> <span className="info-box">10/13/2025</span><br />
                Poor drainage causing severe flooding during rainy season affecting multiple homes.<br />
                Reported by Grace Kimani
              </p>
              <a className="details" href="#">View details →</a>
            </div>
          </article>

          <article className="card">
            <div className="image-section">
              <img src="/ANIMAL.png" alt="Illegal Poaching of Animals" />
            </div>
            <div className="text-section">
              <h3>Illegal Poaching of Animals</h3>
              <p>
                <span className="info-box">Poaching</span> <span className="info-box">Nairobi, Kenya</span> <span className="info-box">10/10/2025</span><br />
                Poaching harms wildlife, disrupts ecosystems, and endangers species survival.<br />
                Reported by Mary Akinyi
              </p>
              <a className="details" href="#">View details →</a>
            </div>
          </article>
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
