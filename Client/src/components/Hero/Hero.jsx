import React from "react";
import "./Hero.css"

const Hero = () => {
  return (
    <section className="hero">
      <div className="hero-content">
        <h1>See the World Through a New<br/>Lens</h1>
        <p>
          EarthLens is an AI-powered platform that empowers you to report environmental issues, 
          gain AI-generated insights, and take meaningful action for a sustainable future.
        </p>
        <p>
          EarthLens simplifies environmental action into three key steps, 
          making it easy for anyone to contribute to a healthier planet.
        </p>
        <a href="/join" className="join-btn">Join Now</a>
      </div>
    </section>
  )
}

export default Hero