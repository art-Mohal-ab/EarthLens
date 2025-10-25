import React from "react";
import "./Contact.css";

const Contact = () => {
  return (
    <div className="contact-container">
      <div className="contact-box">
        <h2>Contact Us</h2>
        <p>We'd love to hear from you. Send us a message and we'll respond as soon as possible.</p>

        <form>
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            placeholder="Your full name"
            required
          />

          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            placeholder="you@example.com"
            required
          />

          <label htmlFor="message">Message</label>
          <textarea
            id="message"
            placeholder="Your message here..."
            rows="5"
            required
          ></textarea>

          <button type="submit" className="contact-btn">Send Message</button>
        </form>

        <div className="contact-info">
          <h3>Get in Touch</h3>
          <p>Email: earthlens@gmail.com</p>
          <p>Phone: +254 700 000 000</p>
        </div>
      </div>
    </div>
  );
};

export default Contact;
