import React, { useState, useRef, useEffect } from 'react';
import './FoodDiary.css';
import { useNavigate } from 'react-router-dom';

const FoodDiary = () => {
  const navigate = useNavigate();
  
  useEffect(() => {
    // Redirect to the new Risk & Food Diary page
    navigate('/risk-food-diary');
  }, [navigate]);
  const [foodEntries, setFoodEntries] = useState([
    {
      id: 1,
      name: 'Mediterranean Salmon Bowl',
      date: '10/02/2025',
      time: '07:30 AM',
      description: 'Baked Salmon fillet, Quinoa, Cucumber and tomato',
      image: null
    },
    {
      id: 2,
      name: 'Chicken and Vegetable Stir-fry',
      date: '10/02/2025',
      time: '12:45 PM',
      description: 'Lean chicken breast, Broccoli, Carrots',
      image: null
    },
    {
      id: 3,
      name: 'Greek Yogurt with Berries',
      date: '10/02/2025',
      time: '06:15 PM',
      description: 'Plain Greek yogurt, Mixed berries (strawberries, blueberries)',
      image: null
    }
  ]);

  const [showNewEntryModal, setShowNewEntryModal] = useState(false);
  const [newEntry, setNewEntry] = useState({
    name: '',
    description: '',
    date: new Date().toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' }),
    time: '',
    image: null
  });
  
  const [riskScore, setRiskScore] = useState(55);
  const fileInputRef = useRef(null);

  const handleAddNewEntry = () => {
    setShowNewEntryModal(true);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewEntry({
      ...newEntry,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const entry = {
      id: foodEntries.length + 1,
      ...newEntry
    };
    setFoodEntries([...foodEntries, entry]);
    setNewEntry({
      name: '',
      description: '',
      date: new Date().toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' }),
      time: '',
      image: null
    });
    setShowNewEntryModal(false);
  };

  const handleCancel = () => {
    setShowNewEntryModal(false);
    setNewEntry({
      name: '',
      description: '',
      date: new Date().toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' }),
      time: '',
      image: null
    });
  };
  
  const handleCapture = () => {
    // Use a camera API
    console.log('Capture photo');
  };
  
  const handleUpload = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };
  
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setNewEntry({
          ...newEntry,
          image: event.target.result
        });
      };
      reader.readAsDataURL(e.target.files[0]);
    }
  };

  return (
    <div className="food-diary-container">
      {/* Home Page Search Bar */}
      {!showNewEntryModal && (
        <div className="food-diary-home">
          <h1 className="food-diary-title">Let's track your meals for better health!</h1>
          <div className="search-bar-container">
            <input 
              type="text" 
              className="search-bar" 
              placeholder="What did you eat today?" 
              onClick={handleAddNewEntry}
            />
          </div>
          <button className="view-history-button" onClick={() => {}}>See My Previous Meals</button>
        </div>
      )}
      
      {/* Weekly Risk Summary */}
      <div className="weekly-risk-summary">
        <div className="risk-summary-header">
          <h2>Weekly Prediabetic Risk Summary</h2>
          <p>This summary is updated on your weekly meal entries. Keep logging your meals for better insights.</p>
        </div>
        
        <div className="risk-summary-content">
          <div className="risk-gauge">
            <div className="risk-circle">
              <svg viewBox="0 0 36 36" className="circular-chart">
                <path className="circle-bg"
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path className="circle"
                  strokeDasharray={`${riskScore}, 100`}
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <text x="18" y="20.35" className="percentage">{riskScore}</text>
              </svg>
            </div>
            <span className="risk-label">Average Risk</span>
          </div>
          
          <div className="risk-advice">
            <p>
              Your food choices this week resulted to an average risk. To stay on track, try to cut down on high-GI foods like white rice and sweets. Choose options like brown rice or sweet potatoes, and add more veggies and protein to your meals. Small changes make a big difference. You're doing great, keep going!
            </p>
          </div>
        </div>
      </div>
      
      {/* Meal History */}
      <div className="meal-history">
        <h2>Your Logged Meals History</h2>
        <h3>Today, {new Date().toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' })}</h3>
        
        <div className="meal-cards-container">

          {/* Meal Entry Modal */}
          {showNewEntryModal && (
            <div className="meal-entry-modal-overlay">
              <div className="meal-entry-modal">
                <div className="modal-header">
                  <h2>Log Meal Entry</h2>
                  <button className="close-button" onClick={handleCancel}>×</button>
                </div>
                <p className="modal-description">Add details for your meal and a photo.</p>
                
                <form onSubmit={handleSubmit}>
                  <div className="form-group">
                    <label>Meal Name</label>
                    <input 
                      type="text" 
                      name="name" 
                      value={newEntry.name} 
                      onChange={handleInputChange} 
                      placeholder="e.g., Nasi Lemak, Laksa, Roti Canai"
                      required 
                    />
                  </div>
                  
                  <div className="form-group">
                    <label>Description</label>
                    <textarea 
                      name="description" 
                      value={newEntry.description} 
                      onChange={handleInputChange} 
                      placeholder="Optionally describe your meal"
                    />
                  </div>
                  
                  <div className="form-group">
                    <label>Time</label>
                    <input 
                      type="time" 
                      name="time" 
                      value={newEntry.time} 
                      onChange={handleInputChange} 
                      required 
                    />
                  </div>
                  
                  <div className="photo-upload-section">
                    <label>Add Photo</label>
                    <div className="photo-area">
                      {newEntry.image ? (
                        <div className="photo-preview">
                          <img src={newEntry.image} alt="Meal preview" />
                        </div>
                      ) : (
                        <div className="no-photo">No photo selected</div>
                      )}
                    </div>
                    <div className="photo-buttons">
                      <button type="button" className="capture-btn" onClick={handleCapture}>
                        <span className="camera-icon">📷</span> Capture
                      </button>
                      <button type="button" className="upload-btn" onClick={handleUpload}>
                        <span className="upload-icon">📤</span> Upload
                      </button>
                      <input 
                        type="file" 
                        ref={fileInputRef} 
                        onChange={handleFileChange} 
                        style={{ display: 'none' }} 
                        accept="image/*" 
                      />
                    </div>
                  </div>
                  
                  <div className="form-actions">
                    <button type="button" className="cancel-btn" onClick={handleCancel}>Cancel</button>
                    <button type="submit" className="save-btn">Save Meal</button>
                  </div>
                </form>
              </div>
            </div>
          )}

          {foodEntries.map((entry) => (
            <div key={entry.id} className="meal-card">
              <div className="meal-card-header">
                <h3>{entry.name}</h3>
                <span className="meal-time">{entry.time}</span>
              </div>
              <div className="meal-card-content">
                {entry.image ? (
                  <img src={entry.image} alt={entry.name} className="meal-image" />
                ) : (
                  <div className="meal-placeholder-image"></div>
                )}
                <p className="meal-description">{entry.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FoodDiary;