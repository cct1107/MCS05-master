import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';
import logo from '../../assets/logo.jpg';

const Navbar = () => {
  const location = useLocation();
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-logo">
          <img src={logo} alt="The Sweet Bit Logo" />
          <span>The Sweet Bit</span>
        </div>
        <div className="navbar-menu">
          <ul className="navbar-items">
            <li className={`navbar-item ${location.pathname === '/' ? 'active' : ''}`}>
              <Link to="/">Home</Link>
            </li>
            <li className={`navbar-item ${location.pathname === '/services' ? 'active' : ''}`}>
              <Link to="/services">What We Provide</Link>
            </li>
            <li className={`navbar-item ${location.pathname === '/risk-food-diary' ? 'active' : ''}`}>
              <Link to="/risk-food-diary">My Risk & Food Diary</Link>
            </li>
            <li className={`navbar-item ${location.pathname === '/log-meal' ? 'active' : ''}`}>
              <Link to="/log-meal">Log My Meal</Link>
            </li>
            <li className={`navbar-item ${location.pathname === '/knowledge' ? 'active' : ''}`}>
              <Link to="/knowledge">Knowledge Corner</Link>
            </li>
          </ul>
        </div>
        <div className="navbar-user">
          <span>Username</span>
          <div className="user-avatar">J</div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;