import React, { useState, useEffect } from 'react';
import { Search, TrendingUp, Sparkles, Eye, Clock, Wand2 } from 'lucide-react';
import axios from 'axios';

export default function TrendsView({ onSelectTrendForGeneration }) {
  const [query, setQuery] = useState('çocuk masalları çizgi film');
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchTrends = async (searchTerm) => {
    setLoading(true);
    try {
      const res = await axios.get(`http://127.0.0.1:8000/api/trends/search?query=${encodeURIComponent(searchTerm)}`);
      setTrends(res.data.results || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrends(query);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchTrends(query);
  };

  return (
    <div style={{ padding: '32px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '24px', fontWeight: 800, fontFamily: 'Outfit', color: '#FFF' }}>
          Trend & Rakip Kanal Araştırması
        </h1>
        <p style={{ color: '#94A3B8', fontSize: '14px', marginTop: '4px' }}>
          YouTube'da en çok izlenen çocuk kanallarını ve viral videoları keşfedin, yapay zeka ile telifsiz ve benzersiz olarak yeniden yorumlayın.
        </p>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="glass-panel" style={{ padding: '16px 24px', display: 'flex', gap: '16px' }}>
        <input 
          className="input-field" 
          style={{ flex: 1, fontSize: '15px' }}
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Trend arama konusu veya rakip kanal adı yazın..."
        />
        <button type="submit" className="btn-primary">
          <Search size={18} /> Araştır
        </button>
      </form>

      {/* Trends Grid */}
      {loading ? (
        <div style={{ padding: '60px', textAlign: 'center', color: '#818CF8', fontSize: '16px' }}>
          YouTube Trendleri Taranaıyor...
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
          {trends.map((t) => (
            <div key={t.id} className="glass-panel" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div style={{
                width: '100%',
                height: '180px',
                borderRadius: '10px',
                overflow: 'hidden',
                background: '#1E293B'
              }}>
                <img src={t.thumbnail} alt={t.title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              </div>

              <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#FFF', lineHeight: '1.4' }}>
                {t.title}
              </h4>

              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#94A3B8' }}>
                <span><Eye size={14} style={{ display: 'inline', verticalAlign: 'middle' }} /> {t.views}</span>
                <span><Clock size={14} style={{ display: 'inline', verticalAlign: 'middle' }} /> {t.published}</span>
              </div>

              <button 
                className="btn-primary" 
                style={{ width: '100%', justifyContent: 'center', marginTop: '4px', fontSize: '13px' }}
                onClick={() => onSelectTrendForGeneration(t.title)}
              >
                <Wand2 size={16} /> AI İle Yeniden Yorumla & Üret
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
