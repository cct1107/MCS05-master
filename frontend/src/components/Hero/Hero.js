import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Hero.css';

const Hero = () => {
  const navigate = useNavigate();
  return (
    <div className="hero">
      <div className="hero-content">
        <h1 className="hero-title">Take Control of Your Health Today<br />and Keep Diabetes At Bay</h1>
        <p className="hero-description">
          Whether its learning more about your condition, asking questions you need
          reliable answers to or getting your health back on track, we're here to help you
          throughout your journey.
        </p>
        <button className="hero-button" onClick={() => navigate('/services')}>Explore</button>
      </div>
      <div className="hero-logo">
        <div className="logo-circle">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="#4CAF50"/>
          </svg>
        </div>
      </div>
    </div>
  );
};

export default Hero;