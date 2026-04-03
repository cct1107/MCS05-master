import React from 'react';
import './Services.css';
import { Link } from 'react-router-dom';
import mealImg from '../../assets/meal.jpg';
import chatbotImg from '../../assets/Chatbot.jpg';
import diagramRAG from '../../assets/diagram-rag.jpg';
import diagramPE from '../../assets/diagram-pe.jpg';

const Services = ({ onAskCoach }) => {
  return (
    <div className="services-page">
      {/* Top section: What we provide */}
      <section className="features-section">
        <h2 className="section-title">What We Provide</h2>
        <div className="cards-grid">
          {/* Chatbot card */}
          <div className="service-card">
            <div className="card-header">
              <h3>Your Personal AI Health Buddy</h3>
              <p>Experience intelligent guidance with our AI-powered chatbot, designed to provide instant support and cuturally relevant health insights.</p>
              <ul className="card-list">
                <li>Cuturally Relevant Advice on Meals</li>
                <li>Nutritional Analysis</li>
                <li>General advice on Prediabetes</li>
                <li>Friendly and Encouraging Support</li>
              </ul>
              <button className="card-button" onClick={onAskCoach}>Ask Your Coach Now</button>
            </div>
            <div className="card-media">
  <img src={chatbotImg} alt="Chatbot preview" style={{ width: '500px', maxWidth: '100%', height: 'auto' }} />
</div>
          </div>

          {/* Food diary card */}
          <div className="service-card">
            <div className="card-header">
              <h3>Effortless Food Tracking & Insights</h3>
              <p>Easily log your meals, track nutritional intake, and gain valuable insights into your eating habits for a healthier lifestyle.</p>
              <ul className="card-list">
                <li>View Meals At A Glance</li>
                <li>Detailed Feedback</li>
                <li>Friendly Suggestions</li>
                <li>Gauge Risk</li>
              </ul>
              <Link to="/food-diary" className="card-button">Start Your Food Diary</Link>
            </div>
            <div className="card-media">
              <img src={mealImg} alt="Food diary preview" />
            </div>
          </div>
        </div>
      </section>

      {/* Technology section */}
      <section className="technology-section">
        <h2 className="section-title">The Brains Behind Our Smart Solutions</h2>
        <p className="section-subtitle">Our platform leverages cutting-edge artificial intelligence to deliver a truly personalized and intelligent health management experience.</p>
        <div className="cards-grid">
          {/* RAG card */}
          <div className="tech-card">
            <div className="tech-card-header">
              <div className="tech-icon">🔗</div>
              <h3>Retrieval-Augmented Generation (RAG)</h3>
              <p>Combining powerful language models with a vast knowledge base ensures our chatbot provides highly accurate, context-rich, and up-to-date health information.</p>
            </div>
            <div className="tech-card-media">
              <img src={diagramRAG} alt="RAG Diagram" style={{ width: '500px', maxWidth: '100%', height: 'auto' }}  />
            </div>
          </div>

          {/* Prompt Engineering card */}
          <div className="tech-card">
            <div className="tech-card-header">
              <div className="tech-icon">✦</div>
              <h3>Advanced Prompt Engineering</h3>
              <p>Through thoughtful prompt design, we tailor the AI to understand nuanced queries and generate clear, effective guidance from your health coach.</p>
            </div>
            <div className="tech-card-media">
              <img src={diagramPE} alt="Prompt Engineering Diagram" style={{ width: '500px', maxWidth: '100%', height: 'auto' }}  />
            </div>
          </div>
<div className="tech-card" style={{ minHeight: 220, maxHeight: 340 }}>
  <div className="tech-card-header">
    <h3>Supported Foods by Our Recognition Module</h3>
    <p>Our system can recognize and analyze these common Malaysian foods:</p>
  </div>
  <div className="foods-table-bg">
    <ul className="foods-table-list">
      <li>Anchovies</li>
      <li>Apam-Balik</li>
      <li>Ayam Rarang</li>
      <li>Blue-Rice</li>
      <li>Char Kuey Teow</li>
      <li>Chicken</li>
      <li>Chicken-Rendang</li>
      <li>Cucumber</li>
      <li>Curry-Puff</li>
      <li>Donat</li>
      <li>Egg</li>
      <li>Fish</li>
      <li>Fried-Chicken</li>
      <li>Fried-Egg</li>
      <li>Fried-Rice</li>
      <li>Hokkien-Mee</li>
      <li>Ikan-Goreng</li>
      <li>Kariayam</li>
      <li>Karipap</li>
      <li>Keropok</li>
      <li>Kuih Lapis</li>
      <li>Kuih Puteri Ayu</li>
      <li>Lo Mein</li>
      <li>Meat</li>
      <li>Mee Rebus</li>
      <li>Mee Siam</li>
      <li>Peanuts</li>
      <li>Rendang</li>
      <li>Rice</li>
      <li>Roti-Canai</li>
      <li>Salad</li>
      <li>Sambal</li>
      <li>Sambaludang</li>
      <li>Sate</li>
      <li>Sauce</li>
      <li>Singgangikan</li>
      <li>Solok lada</li>
      <li>Soup</li>
      <li>Tomatoes</li>
      <li>Wantan Mee</li>
    </ul>
  </div>
</div>
    
 
        </div>
      </section>
    </div>
  );
};

export default Services;