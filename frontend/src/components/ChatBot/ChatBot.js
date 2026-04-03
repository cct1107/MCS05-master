import React, { useState, useRef, useEffect } from 'react';
import './ChatBot.css';

const BACKEND_URL = "http://127.0.0.1:8000";

const ChatBot = ({ isOpen, setIsOpen }) => {

  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'ai',
      text: "Hi! I am your prediabetes assistant. You can ask me anything about prediabetes, blood sugar, or food choices for better health. Please ask one question at a time so I can give you the best and most accurate answer!",
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      feedback: null
    }
  ]);

  
  const [newMessage, setNewMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [showGoogleForm, setShowGoogleForm] = useState(false);
  const [googleFormUrl, setGoogleFormUrl] = useState('');

  const fileInputRef = useRef(null);
  const messagesEndRef = useRef(null);

  const toggleChat = () => setIsOpen(!isOpen);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isTyping]);

  const handleFileSelect = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    setImageFile(f);
    setImagePreview(URL.createObjectURL(f));
  };


  const handleFeedback = (msgId, feedback) => {
  setMessages(prev =>
    prev.map(m =>
      m.id === msgId ? { ...m, feedback } : m
    )
  );
    if (feedback === 'bad') {
      const aiMsg = messages.find(m => m.id === msgId);
      // Find the most recent user message before this AI message
      const aiIdx = messages.findIndex(m => m.id === msgId);
      let userMsg = '';
      for (let i = aiIdx - 1; i >= 0; i--) {
        if (messages[i].sender === 'user') {
          userMsg = messages[i].text;
          break;
        }
      }
      // entry.156947028 = user question, entry.1990929124 = ai respond
      const url = `https://docs.google.com/forms/d/e/1FAIpQLSfHsANfsidkAB-w-bkrkv6pCmlbAkuqY2WG91JFVFnnbn2eJg/viewform?usp=pp_url&entry.156947028=${encodeURIComponent(userMsg)}&entry.1990929124=${encodeURIComponent(aiMsg.text)}`;
      setGoogleFormUrl(url);
      setShowGoogleForm(true);
    }
  };

  const clearSelectedImage = () => {
    setImageFile(null);
    setImagePreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() && !imageFile) return;

    const timestamp = () =>
      new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const userText = newMessage;
    const fileToSend = imageFile;
    const previewToShow = imagePreview;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: userText || (fileToSend ? '(Image only)' : ''),
      image: previewToShow || null,
      time: timestamp()
    };
    setMessages(prev => [...prev, userMsg]);

    setNewMessage('');
    clearSelectedImage();

    setIsTyping(true);

    try {
      let data;
      if (fileToSend) {
        const form = new FormData();
        form.append("query", userText || "Please analyze the foods in the image.");
        form.append("file", fileToSend);
        const res = await fetch(`${BACKEND_URL}/chat/submit`, {
          method: "POST",
          body: form
        });
        if (!res.ok) throw new Error("Upload failed");
        data = await res.json();
      } else {
        const res = await fetch(`${BACKEND_URL}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: userText })
        });
        if (!res.ok) throw new Error("Request failed");
        data = await res.json();
      }

      const aiMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        text: data.reply,
        time: timestamp(),
        feedback: null
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, {
        id: Date.now() + 2,
        sender: 'ai',
        text: 'Request failed. Please try again.',
        time: timestamp(),
        feedback: null
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleCameraCapture = () => {
    if (fileInputRef.current) fileInputRef.current.click();
  };

  return (
    <div className="chatbot-container">
      {!isOpen ? (
        <button className="chatbot-button" onClick={toggleChat}>
          <div className="chatbot-icon">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none"
                 xmlns="http://www.w3.org/2000/svg">
              <path d="M21 11.5C21 16.1944 16.7467 20 11.5 20C10.2281 20 9.02245 19.7775 7.94061 19.3781L4 20.5L5.21147 17.2065C3.85507 15.8758 3 13.8049 3 11.5C3 6.80558 7.25329 3 12.5 3C17.7467 3 21 6.80558 21 11.5Z"
                    stroke="#4CAF50" strokeWidth="2" strokeLinecap="round"
                    strokeLinejoin="round" />
              <circle cx="9" cy="11.5" r="1" fill="#4CAF50" />
              <circle cx="12.5" cy="11.5" r="1" fill="#4CAF50" />
              <circle cx="16" cy="11.5" r="1" fill="#4CAF50" />
            </svg>
          </div>
        </button>
      ) : (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="chatbot-header-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
                   xmlns="http://www.w3.org/2000/svg">
                <path d="M21 11.5C21 16.1944 16.7467 20 11.5 20C10.2281 20 9.02245 19.7775 7.94061 19.3781L4 20.5L5.21147 17.2065C3.85507 15.8758 3 13.8049 3 11.5C3 6.80558 7.25329 3 12.5 3C17.7467 3 21 6.80558 21 11.5Z"
                      stroke="#4CAF50" strokeWidth="2" strokeLinecap="round"
                      strokeLinejoin="round" />
                <circle cx="9" cy="11.5" r="1" fill="#4CAF50" />
                <circle cx="12.5" cy="11.5" r="1" fill="#4CAF50" />
                <circle cx="16" cy="11.5" r="1" fill="#4CAF50" />
              </svg>
            </div>
            <button className="chatbot-close" onClick={toggleChat}>×</button>
          </div>

          <div className="chatbot-messages">
            {messages.map((m, idx) => (
              <div key={m.id} className={`message ${m.sender}`}>
                {m.sender === 'ai' && (
                  <div className="message-avatar ai"><span>AI</span></div>
                )}
                <div className="message-content">
                  {m.image && (
                    <div className="message-image">
                      <img src={m.image} alt="uploaded" />
                    </div>
                  )}
                  <div className="message-text">{m.text}</div>
                  <div className="message-time">{m.time}</div>
                  {/* Feedback buttons */}
                  {m.sender === 'ai' && m.id !== 1 && (
                    <div className="feedback-buttons" style={{ marginTop: 8, display: "flex", alignItems: "center" }}>
                      <button
                        onClick={() => {
                          if (m.feedback === 'bad') {
                            setMessages(prev =>
                              prev.map(msg =>
                                msg.id === m.id ? { ...msg, feedback: null } : msg
                              )
                            );
                          } else {
                            handleFeedback(m.id, 'bad');
                          }
                        }}
                        style={{
                          background: m.feedback === 'bad' ? '#f44336' : '#eee',
                          color: m.feedback === 'bad' ? '#fff' : '#333',
                          border: 'none',
                          borderRadius: '16px',
                          padding: '4px 14px',
                          fontWeight: 'bold',
                          cursor: 'pointer'
                        }}
                      >👎 Not helpful</button>
                    </div>
                  )}
                </div>
                {m.sender === 'user' && (
                  <div className="message-avatar user"><span>U</span></div>
                )}
              </div>
            ))}

            {isTyping && (
              <div className="message ai typing">
                <div className="message-avatar ai"><span>AI</span></div>
                <div className="message-content">
                  <div className="message-text">AI is typing...</div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chatbot-input" onSubmit={handleSendMessage}>
            <input
              type="text"
              placeholder="Type a message here"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              disabled={isTyping}
            />
            {imagePreview && (
              <div className="image-preview">
                <img src={imagePreview} alt="preview" style={{ maxHeight: 80 }} />
                <button type="button" onClick={clearSelectedImage}>✕</button>
              </div>
            )}
            <div className="chatbot-actions">
              <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                accept="image/*"
                onChange={handleFileSelect}
              />
              <button type="button" className="action-button" onClick={handleCameraCapture} disabled={isTyping}>
                <span role="img" aria-label="camera">📷</span>
              </button>
              <button type="submit" className="action-button send" disabled={isTyping}>
                <span role="img" aria-label="send">📤</span>
              </button>
            </div>
          </form>
        </div>
      )}
      {showGoogleForm && (
        <div className="feedback-modal-overlay">
          <div className="feedback-modal" style={{ width: 480, height: 600, padding: 0 }}>
            <button
              style={{
                position: "absolute", top: 10, right: 16, zIndex: 2, background: "#fff", border: "none", fontSize: 22, cursor: "pointer"
              }}
              onClick={() => setShowGoogleForm(false)}
              aria-label="Close"
            >×</button>
            <iframe
              src={googleFormUrl}
              title="Feedback"
              width="100%"
              height="100%"
              style={{ border: "none", borderRadius: 12 }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatBot;