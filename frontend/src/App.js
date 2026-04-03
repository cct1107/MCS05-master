import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar/Navbar';
import Hero from './components/Hero/Hero';
import ChatBot from './components/ChatBot/ChatBot';
import FoodDiary from './components/FoodDiary/FoodDiary';
import LogMeal from './components/LogMeal/LogMeal';
import RiskFoodDiary from './components/RiskFoodDiary/RiskFoodDiary';
import Services from './components/Services/Services';
import Knowledge from './components/Knowledge/Knowledge';

function App() {
  const [chatOpen, setChatOpen] = useState(false);

  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Hero />} />
          <Route path="/food-diary" element={<FoodDiary />} />
          <Route path="/log-meal" element={<LogMeal />} />
          <Route path="/risk-food-diary" element={<RiskFoodDiary />} />
          <Route path="/services" element={<Services onAskCoach={() => setChatOpen(true)} />} />
          <Route path="/knowledge" element={<Knowledge />} />
        </Routes>
        <ChatBot isOpen={chatOpen} setIsOpen={setChatOpen} />
      </div>
    </Router>
  );
}

export default App;