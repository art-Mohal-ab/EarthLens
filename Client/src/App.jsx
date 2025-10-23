import React from "react";
import Navbar from "./components/Navbar/Navbar";
import Hero from "./components/Hero/Hero";
import Cards from "./components/Cards/Cards";
import IssueCards from "./components/IssueCards/IssueCards";
import Footer from "./components/Footer/Footer";

const App = () => {
  return (
    <div className="app">
      <Navbar />
      <main>
        <Hero />
        <Cards />
        <IssueCards/>
      </main>
      <Footer />
    </div>
  );
};

export default App;