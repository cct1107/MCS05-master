import React, { useMemo, useState } from 'react';
import './Knowledge.css';
import knowledgeItems from './knowledgeData';

const categories = ['All', 'Prediabetes', 'Nutrition'];

const Knowledge = () => {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('All');
  const [activeItem, setActiveItem] = useState(null);

  const filteredItems = useMemo(() => {
    return knowledgeItems.filter((item) => {
      const matchesCategory = category === 'All' || item.category === category;
      const q = query.trim().toLowerCase();
      const matchesQuery = !q || item.title.toLowerCase().includes(q) || item.description.toLowerCase().includes(q);
      return matchesCategory && matchesQuery;
    });
  }, [query, category]);

  return (
    <div className="knowledge-page">
      <header className="knowledge-header">
        <h1>Knowledge Corner</h1>
        <p className="subtitle">Curated readings on prediabetes and nutrition — simple, organized, and distraction‑free.</p>
        <div className="controls">
          <input
            className="search"
            type="text"
            placeholder="Search topics…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <div className="chips">
            {categories.map((c) => (
              <button
                key={c}
                className={`chip ${category === c ? 'active' : ''}`}
                onClick={() => setCategory(c)}
              >
                {c}
              </button>
            ))}
          </div>
        </div>
      </header>

      <main className="grid">
        {filteredItems.map((item, i) => (
          <article key={i} className="doc-card">
            <div className="doc-meta">
              <span className="badge">{item.category}</span>
              <h3 className="doc-title">{item.title}</h3>
              <p className="doc-desc">{item.description}</p>
            </div>
            <div className="doc-actions">
              <button className="view" onClick={() => setActiveItem(item)}>View</button>
            </div>
          </article>
        ))}
      </main>

      {/* Modal viewer */}
      {activeItem && (
        <div className="modal" role="dialog" aria-modal="true">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{activeItem.title}</h3>
              <button className="close" onClick={() => setActiveItem(null)} aria-label="Close">×</button>
            </div>
            <div className="modal-body">
              <iframe
                title={activeItem.title}
                src={activeItem.pdfUrl}
                className="pdf-frame"
              />
            </div>
          </div>
          <div className="modal-backdrop" onClick={() => setActiveItem(null)} />
        </div>
      )}
    </div>
  );
};

export default Knowledge;