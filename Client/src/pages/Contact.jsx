import React from "react";
import "./Contact.css";

const Contact = () => {
  return (
    <div className="contact-container">
      <div className="contact-header">
        <h2>Contact Us</h2>
        <p>Fill in your information below and we will reach out</p>
      </div>

      <div className="contact-content">
        <form className="contact-form">
          <label htmlFor="email">Your Email:</label>
          <input
            type="email"
            id="email"
            placeholder="you@example.com"
            required
          />

          <label htmlFor="category">Category:</label>
          <input
            type="text"
            id="category"
            placeholder="Select a category"
            required
          />

          <label htmlFor="message">Message:</label>
          <textarea id="message" placeholder="Write your message..." required />

          <button type="submit" className="send-btn">
            Send Message
          </button>
        </form>

        <div className="contact-info">
          <div className="info-box">
            <h3>Email Support</h3>
            <p>Support@gmail.com</p>
          </div>

          <div className="info-box">
            <h3>Phone</h3>
            <p>+254 113 034 076</p>
          </div>

          <div className="info-box">
            <h3>Office</h3>
            <p>
              Nairobi, Kenya <br />
              1st Floor, Westlands
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;
