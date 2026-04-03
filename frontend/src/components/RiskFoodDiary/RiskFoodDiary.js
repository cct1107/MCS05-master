import React, { useState, useEffect } from 'react';
import './RiskFoodDiary.css';
import { Link, useLocation } from 'react-router-dom';

const RiskFoodDiary = () => {
  const location = useLocation();
  const [riskScore, setRiskScore] = useState(0);
  const [weeklySummary, setWeeklySummary] = useState('');
  const [foodEntries, setFoodEntries] = useState([]);
  const [modalEntry, setModalEntry] = useState(null);
  const [deleteMode, setDeleteMode] = useState(false);
  const [selectedIds, setSelectedIds] = useState([]);
  const [isGeneratingSummary, setIsGeneratingSummary] = useState(false);
  const today = new Date();
  const weekAgo = new Date(today);

  const sortedEntries = [...foodEntries].sort((a, b) => {
    if (!a.date) return 1;
    if (!b.date) return -1;

    const aDateTime = new Date(`${a.date}T${a.time || '00:00'}`);
    const bDateTime = new Date(`${b.date}T${b.time || '00:00'}`);
    return bDateTime - aDateTime;
  });
  weekAgo.setDate(today.getDate() - 6);
  const thisWeekEntries = sortedEntries.filter(entry => {
      const mealDate = entry.date ? new Date(entry.date) : null;
      return mealDate && mealDate >= weekAgo;
    });

    const otherEntries = sortedEntries.filter(entry => {
      const mealDate = entry.date ? new Date(entry.date) : null;
      return !mealDate || mealDate < weekAgo;
    });

  // load saved data on mount
  useEffect(() => {
    const savedMeals = JSON.parse(localStorage.getItem('mealEntries')) || [];
    setFoodEntries(savedMeals);

    const savedRisk = localStorage.getItem('riskScore');
    if (savedRisk) setRiskScore(Number(savedRisk));

    const savedSummary = localStorage.getItem('weeklySummary');
    if (savedSummary) setWeeklySummary(savedSummary);

    if (localStorage.getItem('isGeneratingSummary') === 'true') {
      setIsGeneratingSummary(true);
    }
  }, []);

  // poll server processing flag -> sync to localStorage + UI
  useEffect(() => {
    let mounted = true;
    const poll = async () => {
      try {
        const res = await fetch('http://localhost:8000/processing-status');
        if (!res.ok) return;
        const data = await res.json();
        if (!mounted) return;
        const serverProcessing = !!data.aiprocessing;
        localStorage.setItem('isGeneratingSummary', serverProcessing ? 'true' : 'false');
        setIsGeneratingSummary(serverProcessing);
      } catch (e) {
        // ignore network errors for polling
      }
    };
    poll();
    const iv = setInterval(poll, 200);
    return () => { mounted = false; clearInterval(iv); };
  }, []);

  // process new meal (from navigation state) or resume from localStorage
  useEffect(() => {
    const newMealFromLocation = location.state?.newMeal;
    const storedFlag = localStorage.getItem('isGeneratingSummary') === 'true';
    let storedProcessing = null;
    try {
      storedProcessing = JSON.parse(localStorage.getItem('processingMeal'));
    } catch (e) {
      storedProcessing = null;
    }
    const mealToProcess = newMealFromLocation || (storedFlag && storedProcessing) || null;
    if (!mealToProcess) return;

    const existing = JSON.parse(localStorage.getItem('mealEntries')) || [];

    // if already processed (has analysis) clear flags and return
    const alreadyProcessed = existing.find(m => m.id === mealToProcess.id && m.analysis);
    if (alreadyProcessed) {
      localStorage.removeItem('processingMeal');
      localStorage.setItem('isGeneratingSummary', 'false');
      window.history.replaceState({}, document.title, window.location.pathname);
      setIsGeneratingSummary(false);
      return;
    }

    const attemptedKey = `processingAttempted_${mealToProcess.id}`;
    // if already attempted, don't re-call backend
    if (localStorage.getItem(attemptedKey) === 'true') {
      setIsGeneratingSummary(localStorage.getItem('isGeneratingSummary') === 'true');
      window.history.replaceState({}, document.title, window.location.pathname);
      return;
    }

    const processNewMeal = async () => {
      setIsGeneratingSummary(true);
      localStorage.setItem(attemptedKey, 'true');

      // ensure meal present in localStorage so UI shows it while processing
      const mealEntries = [...existing.filter(m => m.id !== mealToProcess.id), mealToProcess];
      localStorage.setItem('mealEntries', JSON.stringify(mealEntries));
      setFoodEntries(mealEntries);
      localStorage.setItem('processingMeal', JSON.stringify(mealToProcess));
      localStorage.setItem('isGeneratingSummary', 'true');

      // prepare recentMeals (7 days)
      const today = new Date();
      const weekAgo = new Date(today);
      weekAgo.setDate(today.getDate() - 6);
      const recentMeals = mealEntries.filter(meal => {
        if (!meal.date) return false;
        const mealDate = new Date(`${meal.date}T00:00:00`);
        return mealDate >= weekAgo && mealDate <= today;
      });

      try {
        const res = await fetch('http://localhost:8000/meals/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: mealToProcess.name,
            description: mealToProcess.description,
            date: mealToProcess.date,
            time: mealToProcess.time,
            file: mealToProcess.image,
            recent_meals: recentMeals
          })
        });

        if (res.status === 409) {
          alert('Server is processing another request. Your meal will be processed when ready.');
          setIsGeneratingSummary(true);
          return;
        }

        const data = await res.json();

        if (data && data.success && data.meal) {
          const updatedEntries = (JSON.parse(localStorage.getItem('mealEntries')) || []).map(m =>
            m.id === mealToProcess.id ? { ...m, nutrition_info: data.meal.nutrition_info, analysis: data.meal.analysis } : m
          );
          localStorage.setItem('mealEntries', JSON.stringify(updatedEntries));
          setFoodEntries(updatedEntries);

          if (data.summary) {
            setWeeklySummary(data.summary);
            localStorage.setItem('weeklySummary', data.summary);
          }
          if (data.score !== undefined) {
            setRiskScore(data.score);
            localStorage.setItem('riskScore', data.score);
          }

          // success -> clear processing flags & attempted marker
          localStorage.removeItem('processingMeal');
          localStorage.setItem('isGeneratingSummary', 'false');
          localStorage.removeItem(attemptedKey);
          setIsGeneratingSummary(false);
        } else {
          const sRes = await fetch('http://127.0.0.1:8000/meals/weekly-summary', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ meals: recentMeals })
          });
          const sData = await sRes.json();
          if (sData.summary) {
            setWeeklySummary(sData.summary);
            localStorage.setItem('weeklySummary', sData.summary);
          }
          if (sData.score !== undefined) {
            setRiskScore(sData.score);
            localStorage.setItem('riskScore', sData.score);
          }

          setIsGeneratingSummary(localStorage.getItem('isGeneratingSummary') === 'true');
          alert('Processing finished but no summary/score returned. It will not auto-retry.');
        }
      } catch (err) {
        console.error('Failed to add meal or fetch summary:', err);
        setIsGeneratingSummary(localStorage.getItem('isGeneratingSummary') === 'true');
        alert('Network or server error while processing the meal. Return later to retry.');
      } finally {
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    };

    processNewMeal();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.state]);

  const getRiskColor = (entry) => {
  if (!entry.analysis || !entry.analysis.rating) return "#ececec";
  if (entry.analysis.rating === "poor") return "#f44336";
  if (entry.analysis.rating === "average") return "#ff9800";
  if (entry.analysis.rating === "good") return "#4caf50";
  return "#ececec";
};

  useEffect(() => {
  if (!isGeneratingSummary) {
    const updatedMeals = JSON.parse(localStorage.getItem('mealEntries')) || [];
    const updatedSummary = localStorage.getItem('weeklySummary') || '';
    const updatedRisk = Number(localStorage.getItem('riskScore')) || 0;

    setFoodEntries(updatedMeals);
    setWeeklySummary(updatedSummary);
    setRiskScore(updatedRisk);
  }
}, [isGeneratingSummary]);

  let riskColor = "#4caf50";
  let riskLabel = "Low Risk";
  if (riskScore > 53 && riskScore <= 80) {
    riskColor = "#ff9800";
    riskLabel = "Average Risk";
  } else if (riskScore > 80) {
    riskColor = "#f44336";
    riskLabel = "High Risk";
  }

  const handleDeleteMode = () => {
    setDeleteMode(true);
    setSelectedIds([]);
  };

  const handleSelect = (id) => {
    setSelectedIds(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  const handleConfirmDelete = async () => {
    // guard: prevent delete while AI processing on server or front-end
    const serverProcessing = localStorage.getItem('isGeneratingSummary') === 'true';
    if (isGeneratingSummary || serverProcessing) {
      alert('AI is processing. Delete is disabled until processing finishes.');
      return;
    }
    
    
    const newEntries = foodEntries.filter(entry => !selectedIds.includes(entry.id));
    setFoodEntries(newEntries);

    // persist processing flag so returning to page shows processing state
    localStorage.setItem('mealEntries', JSON.stringify(newEntries));
    localStorage.setItem('isGeneratingSummary', 'true');
    localStorage.setItem('deleteMode', 'true');
    setIsGeneratingSummary(true);

    setDeleteMode(false);
    setSelectedIds([]);

    const today = new Date();
    const weekAgo = new Date(today);
    weekAgo.setDate(today.getDate() - 6);
    const recentMeals = newEntries.filter(meal => {
      if (!meal.date) return false;
      const mealDate = new Date(`${meal.date}T00:00:00`);
      return mealDate >= weekAgo && mealDate <= today;
    });

    try {
      const res = await fetch('http://127.0.0.1:8000/meals/weekly-summary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ meals: recentMeals })
      });
      const data = await res.json();
      if (data.summary) {
        setWeeklySummary(data.summary);
        localStorage.setItem('weeklySummary', data.summary);
      }
      if (data.score !== undefined) {
        setRiskScore(data.score);
        localStorage.setItem('riskScore', data.score);
      }
    } catch (e) {
      alert('Failed to update weekly summary!');
    } finally {
      // clear processing flag on finish (success or failure)
      setIsGeneratingSummary(false);
      localStorage.setItem('isGeneratingSummary', 'false');
      localStorage.setItem('deleteMode', 'false');
    }
  };

  const handleCancelDelete = () => {
    setDeleteMode(false);
    setSelectedIds([]);
  };

  const renderMealCard = (entry) => (
    <div
      key={entry.id}
      className="meal-card"
      style={{ cursor: deleteMode ? 'default' : 'pointer', position: "relative" }}
      onClick={() => !deleteMode && setModalEntry(entry)}
      title={deleteMode ? "" : "Click to view nutrition info"}
    >
      {deleteMode && (
        <input
          type="checkbox"
          className="delete-checkbox"
          checked={selectedIds.includes(entry.id)}
          onChange={() => handleSelect(entry.id)}
          style={{
            position: "absolute",
            top: 12,
            right: 12,
            width: 22,
            height: 22,
            zIndex: 2
          }}
        />
      )}
      <div className="meal-card-header" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h3>{entry.name}</h3>
        <div style={{ textAlign: "right" }}>
          <div
            className="meal-date-time-box"
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              width: 110,
              height: 48,
              background: (() => {
                const today = new Date();
                const weekAgo = new Date(today);
                weekAgo.setDate(today.getDate() - 6);
                const mealDate = entry.date ? new Date(entry.date) : null;
                if (mealDate && mealDate < weekAgo) return "#eee";
                return "#f5f3e7";
              })(),
              borderRadius: "12px",
              marginLeft: 8,
              fontSize: "1em",
              fontWeight: 500,
              color: "#bba96b",
              textAlign: "center"
            }}
          >
            {entry.date && (
              <>
                <span style={{ display: "block", width: "100%" }}>
                  {new Date(entry.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}
                </span>
                <span style={{ display: "block", width: "100%" }}>
                  {entry.time}
                </span>
              </>
            )}
          </div>
        </div>
      </div>
      <div className="meal-card-content">
        {entry.image ? (
          <img src={entry.image} alt={entry.name} className="meal-image" />
        ) : (
          <img
            src={`https://source.unsplash.com/random/300x200/?${entry.name.split(' ')[0].toLowerCase()}`}
            alt={entry.name}
            className="meal-image"
          />
        )}
        <div className="meal-ingredients">
          {entry.description ? (
            entry.description.split('\n').map((line, index) => (
              <p key={index}>{line}</p>
            ))
          ) : (
            <p>No ingredients listed</p>
          )}
        </div>
      </div>
    </div>
  );


  return (
    <div className="risk-food-diary-container">
      <div className="risk-food-diary-header">
        <h1 className="risk-food-diary-title">My Risk & Food Diary</h1>
        <Link
          to="/log-meal"
          className="log-meal-button"
          style={isGeneratingSummary ? { pointerEvents: 'none', opacity: 0.6 } : {}}
        >
          Log a New Meal
        </Link>
      </div>

      {/* Weekly Risk Summary */}
      <div className="weekly-risk-summary">
        <div className="risk-summary-header">
          <h2>Weekly Prediabetic Risk Summary</h2>
          <p>This summary is updated on your weekly meal entries. Keep logging your meals for better insights.</p>
        </div>

        <div className="risk-summary-content">
          <div className="risk-gauge">
            <div className={`risk-circle ${isGeneratingSummary ? 'rotating' : ''}`}>
              {/* keep circle layout but when processing show rotating green arc */}
              <svg viewBox="0 0 36 36" className="circular-chart">
                <path
                  className="circle-bg"
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className="circle"
                  strokeDasharray={isGeneratingSummary ? `30, 100` : `${riskScore}, 100`}
                  style={{ stroke: isGeneratingSummary ? '#4caf50' : riskColor }}
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <text x="18" y="18" className="percentage">
                  {isGeneratingSummary ? '' : riskScore}
                </text>
              </svg>
            </div>
            <div
              className="risk-label"
              style={{
                color: isGeneratingSummary ? '#ff9800' : riskColor,
                minHeight: 24,
                fontWeight: isGeneratingSummary ? 600 : 500
              }}
            >
              {isGeneratingSummary ? 'AI processing...' : riskLabel}
            </div>
          </div>

          <div className="risk-advice" style={{ minWidth: 420, minHeight: 120, paddingLeft: 24 }}>
            <p style={{ margin: 0, color: '#666' }}>
              {isGeneratingSummary ? 'AI is generating your summary and score...' : weeklySummary}
            </p>
          </div>
        </div>
      </div>

      {/* Meal History */}
      <div className="meal-history">
        <div className="meal-history-header" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 8 }}>
          <div>
            <h2 style={{ margin: 0 }}>Your Logged Meals History</h2>
            <h3 style={{ margin: 0, fontWeight: 400, fontSize: "1.1em", color: "#888" }}>
              Today, {new Date().toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' })}
            </h3>
          </div>
          <button
            className="log-meal-button"
            style={{ background: "#f44336", minWidth: 90, opacity: isGeneratingSummary ? 0.6 : 1, pointerEvents: isGeneratingSummary ? 'none' : 'auto' }}
            onClick={handleDeleteMode}
            disabled={deleteMode || isGeneratingSummary}
          >
            Delete Meals
          </button>
        </div>

          {sortedEntries.length === 0 ? (
            <p>No meals logged yet.</p>
          ) : (
            <>
              {/* This Week */}
              {thisWeekEntries.length > 0 && (
                <div style={{ marginBottom: "24px" }}>
                  <h3 style={{ margin: "16px 0 8px 0" }}>This Week:</h3>
                  <div className="meal-cards-row">
                    {thisWeekEntries.map(entry => renderMealCard(entry))}
                  </div>
                </div>
              )}

              {/* Earlier Meals */}
              {otherEntries.length > 0 && (
                <div style={{ marginBottom: "16px" }}>
                  <h3 style={{ margin: "16px 0 8px 0" }}>Earlier Meals:</h3>
                  <div className="meal-cards-row">
                    {otherEntries.map(entry => renderMealCard(entry))}
                  </div>
                </div>
              )}
            </>
          )}


        {deleteMode && (
          <div style={{ marginTop: 24, display: "flex", gap: 16 }}>
            <button
              className="log-meal-button"
              style={{ background: "#f44336" }}
              onClick={handleConfirmDelete}
              disabled={selectedIds.length === 0 || isGeneratingSummary}
            >
              Confirm Delete
            </button>
            <button
              className="log-meal-button"
              style={{ background: "#888" }}
              onClick={handleCancelDelete}
            >
              Cancel
            </button>
          </div>
        )}
      </div>

      {/*  nutrition_info */}
      {modalEntry && (
        <div className="nutrition-info-modal-overlay" onClick={() => setModalEntry(null)}>
          <div className="nutrition-info-modal" onClick={e => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setModalEntry(null)}>×</button>
            <h4>Nutrition Analysis</h4>
            {modalEntry.analysis ? (
              <table>
                <thead>
                  <tr>
                    <th>Rating</th>
                    <th>Reason</th>
                    <th>Tip</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style={{
                      color:
                        modalEntry.analysis.rating === "poor"
                          ? "#f44336"
                          : modalEntry.analysis.rating === "average"
                          ? "#ff9800"
                          : "#4caf50",
                      fontWeight: "bold",
                      textTransform: "capitalize"
                    }}>
                      {modalEntry.analysis.rating}
                    </td>
                    <td>{modalEntry.analysis.reason}</td>
                    <td>{modalEntry.analysis.tip}</td>
                  </tr>
                </tbody>
              </table>
            ) : (
              <p>No nutrition analysis available.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default RiskFoodDiary;