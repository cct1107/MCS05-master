import React, { useState, useRef, useEffect } from 'react';
import './LogMeal.css';
import { Link, useNavigate } from 'react-router-dom';

const LogMeal = () => {
  const navigate = useNavigate();
  const [showNewEntryModal, setShowNewEntryModal] = useState(false);
  const [serverProcessing, setServerProcessing] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false); 
  const [timeError, setTimeError] = useState('');

  const [newEntry, setNewEntry] = useState({
    name: '',
    description: '',
    date: getLocalTodayStr(), 
    time: new Date().toTimeString().split(' ')[0].slice(0, 5),
    image: null
  });
  const fileInputRef = useRef(null);
  const [deleteMode, setDeleteMode] = useState(false);
  useEffect(() => {
    const checkDeleteMode = () => {
      setDeleteMode(localStorage.getItem('deleteMode') === 'true');
    };
    checkDeleteMode();
    const iv = setInterval(checkDeleteMode, 200);
    return () => clearInterval(iv);
  }, []);

    // poll backend processing flag so submit button can reflect server-side state
 useEffect(() => {
  let mounted = true;
  const check = async () => {
    try {
      const res = await fetch('http://localhost:8000/processing-status');
      if (!res.ok) return;
      const data = await res.json();
      if (!mounted) return;
      setServerProcessing(!!data.aiprocessing);
    } catch (e) {
      // ignore
    }
  };
  check();
  const iv = setInterval(check, 200);
  return () => { mounted = false; clearInterval(iv); };
}, []);

  const handleAddNewEntry = () => {
    setShowNewEntryModal(true);
  };

  function getLocalTodayStr() {
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const dd = String(now.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
  }

  const handleCancel = () => {
    setShowNewEntryModal(false);
    setNewEntry({
      name: '',
      description: '',
      date: new Date().toISOString().split('T')[0],
      time: new Date().toTimeString().split(' ')[0].slice(0, 5),
      image: null
    });
  };

  function getLocalTodayStr() {
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const dd = String(now.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
  }
  const todayStr = getLocalTodayStr();

  const handleSubmit = (e) => {
    
    e.preventDefault();
    const hasDescription = !!(newEntry.description && newEntry.description.trim());
    const hasImage = !!(newEntry.image || (fileInputRef.current && fileInputRef.current.files && fileInputRef.current.files[0]));
    if (!hasDescription && !hasImage) {
      alert('Please provide a description or upload a photo (at least one of description or photo is required).');
      return;
    }
    
    if (isProcessing) return;
    const mealData = {
      ...newEntry,
      id: Date.now(),
      image: newEntry.image 
    };

    setIsProcessing(false);
    setShowNewEntryModal(false);
    navigate('/risk-food-diary', { state: { newMeal: mealData } });
  };

  const handleInputChange = (e) => {
    
    const { name, value } = e.target;
    if (name === "time" || name === "date") {
      const dateToCheck = name === "date" ? value : newEntry.date;
      const timeToCheck = name === "time" ? value : newEntry.time;
      if (dateToCheck === todayStr) {
        const now = new Date();
        const [hh, mm] = timeToCheck.split(":");
        const selected = new Date();
        selected.setHours(Number(hh));
        selected.setMinutes(Number(mm));
        selected.setSeconds(0);
        selected.setMilliseconds(0);
        if (selected > now) {
          setTimeError("Time cannot be in the future.");
        } else {
          setTimeError('');
        }
      } else {
        setTimeError('');
      }
    }
    setNewEntry(prev => ({ ...prev, [name]: value }));
  };



  const handleUpload = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onloadend = () => {
        setNewEntry(prev => ({ ...prev, image: reader.result }));
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="log-meal-container">
      <div className="log-meal-home">
        <h1 className="log-meal-title">Let's track your meals for better health!</h1>
        
        <div className="search-bar-container">
          <input 
            type="text" 
            className="search-bar" 
            placeholder="What did you eat today?" 
            onClick={handleAddNewEntry}
          />
        </div>
        
        <button className="view-history-button" onClick={() => window.location.href = '/risk-food-diary'}>
          See My Previous Meals
        </button>
      </div>
      {/* AI Processing Modal */}
      {isProcessing && (
        <div className="ai-processing-modal-overlay">
          <div className="ai-processing-modal">
            <div className="spinner" />
            <p>AI is analyzing your meal and generating your summary.<br />Please wait...</p>
          </div>
        </div>
      )}

      {/* Meal Entry Modal */}
      {showNewEntryModal && (
        <div className="meal-entry-modal-overlay">
          <div className="meal-entry-modal">
            <div className="modal-header">
              <h2>Log a New Meal</h2>
              <button className="close-button" onClick={handleCancel}>&times;</button>
            </div>
            <p className="modal-description">Record what you ate to track your dietary habits</p>
            
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="name">Meal Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={newEntry.name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="description">Description</label>
                <textarea
                  id="description"
                  name="description"
                  value={newEntry.description}
                  onChange={handleInputChange}
                  placeholder="What ingredients did your meal contain?"
                ></textarea>
                <div className="description-hint" style={{ fontSize: '0.95em', color: '#888', marginTop: '6px' }}>
                  Since our image recognition database is limited — see Our What We Provide — the more precise your ingredients and portion details, the more accurate your score will be.
                </div>
              </div>

              <div className="form-group">
                  <label htmlFor="date">Date</label>
                  <input
                    type="date"
                    id="date"
                    name="date"
                    value={newEntry.date}
                    onChange={handleInputChange}
                    max={todayStr}
                    required
                  />
                </div>
              
              <div className="form-group">
                <label htmlFor="time">Time</label>
                <input
                  type="time"
                  id="time"
                  name="time"
                  value={newEntry.time}
                  onChange={handleInputChange}
                  required
                  max={newEntry.date === todayStr ? new Date().toTimeString().slice(0,5) : undefined}
                  style={{
                    borderColor: timeError ? '#f44336' : undefined,
                    background: timeError ? '#fff6f6' : undefined
                  }}
                />
                {timeError && (
                  <div style={{ color: '#f44336', fontSize: '0.95em', marginTop: 4 }}>
                    {timeError}
                  </div>
                )}
              </div>
              
              <div className="photo-upload-section">
                <label>Photo</label>
                <div className="photo-area">
                  {newEntry.image ? (
                    <div className="photo-preview">
                      <img src={newEntry.image} alt="Meal preview" />
                    </div>
                  ) : (
                    <div className="no-photo">No photo added yet</div>
                  )}
                </div>
                
                <div className="photo-buttons">
                  <button 
                    type="button" 
                    className="upload-btn"
                    onClick={handleUpload}
                  >
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
                <button
                  type="submit"
                  className="save-btn"
                  disabled={isProcessing || !!timeError || serverProcessing || deleteMode}
                >
                  {isProcessing ? 'Saving...' : 'Save Meal'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default LogMeal;