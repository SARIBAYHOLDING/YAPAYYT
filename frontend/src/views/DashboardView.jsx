import React from 'react';
import { 
  Tv, 
  Video, 
  Zap, 
  Sparkles, 
  ArrowUpRight, 
  CheckCircle, 
  Clock, 
  Plus, 
  TrendingUp,
  Play
} from 'lucide-react';

export default function DashboardView({ channels, videos, onNavigate }) {
  const activeAutopilotCount = channels.filter(c => c.auto_pilot === 1).length;

  return (
    <div style={{ padding: '32px', display: 'flex', flexDirection: 'column', gap: '28px' }}>
      
      {/* Welcome Banner */}
      <div className="glass-panel" style={{
        padding: '28px 32px',
        background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%)',
        border: '1px solid rgba(129, 140, 248, 0.3)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div>
          <span style={{ fontSize: '12px', fontWeight: 700, color: '#818CF8', letterSpacing: '1px', textTransform: 'uppercase' }}>
            Sarıbay Yazılım YouTube Fabrikası
          </span>
          <h1 style={{ fontSize: '26px', fontWeight: 800, fontFamily: 'Outfit', color: '#FFF', marginTop: '6px' }}>
            Hoş Geldiniz, Selahattin Sarıbay 👋
          </h1>
          <p style={{ color: '#94A3B8', fontSize: '14px', marginTop: '4px', maxWidth: '650px' }}>
            Tam otonom, sıfır maliyetli yapay zeka YouTube sisteminiz aktif. Kanallarınız için otomatik senaryo, seslendirme, AI görsel ve video üretimi gerçekleşmektedir.
          </p>
        </div>

        <button className="btn-primary" onClick={() => onNavigate('generator')}>
          <Sparkles size={18} /> Anında Video Üret
        </button>
      </div>

      {/* Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px' }}>
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748B' }}>
            <span style={{ fontSize: '13px', fontWeight: 600 }}>Aktif Kanallar</span>
            <Tv size={20} color="#818CF8" />
          </div>
          <div style={{ fontSize: '32px', fontWeight: 800, fontFamily: 'Outfit', color: '#FFF', marginTop: '10px' }}>
            {channels.length}
          </div>
          <div style={{ fontSize: '12px', color: '#34D399', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <CheckCircle size={12} /> {activeAutopilotCount} Kanal Otomatik Modda
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748B' }}>
            <span style={{ fontSize: '13px', fontWeight: 600 }}>Üretilen Videolar</span>
            <Video size={20} color="#F59E0B" />
          </div>
          <div style={{ fontSize: '32px', fontWeight: 800, fontFamily: 'Outfit', color: '#FFF', marginTop: '10px' }}>
            {videos.length}
          </div>
          <div style={{ fontSize: '12px', color: '#94A3B8', marginTop: '4px' }}>
            Shorts & Uzun Format
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748B' }}>
            <span style={{ fontSize: '13px', fontWeight: 600 }}>Üretim Maliyeti</span>
            <Zap size={20} color="#34D399" />
          </div>
          <div style={{ fontSize: '32px', fontWeight: 800, fontFamily: 'Outfit', color: '#34D399', marginTop: '10px' }}>
            0.00 TL
          </div>
          <div style={{ fontSize: '12px', color: '#94A3B8', marginTop: '4px' }}>
            Edge TTS & Pollinations AI
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748B' }}>
            <span style={{ fontSize: '13px', fontWeight: 600 }}>Sistem Durumu</span>
            <CheckCircle size={20} color="#10B981" />
          </div>
          <div style={{ fontSize: '20px', fontWeight: 700, fontFamily: 'Outfit', color: '#FFF', marginTop: '14px' }}>
            Tam Otonom
          </div>
          <div style={{ fontSize: '12px', color: '#34D399', marginTop: '4px' }}>
            Arka Plan Scheduler Çalışıyor
          </div>
        </div>
      </div>

      {/* Main Grid: Channels & Quick Production */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        
        {/* Left Column: Recent Generated Videos */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h3 style={{ fontSize: '18px', fontWeight: 700, fontFamily: 'Outfit', color: '#FFF' }}>
              Son Üretilen Videolar
            </h3>
            <button className="btn-secondary" style={{ fontSize: '12px', padding: '6px 12px' }} onClick={() => onNavigate('studio')}>
              Tümünü Gör
            </button>
          </div>

          {videos.length === 0 ? (
            <div style={{ padding: '40px 20px', textAlign: 'center', color: '#64748B' }}>
              <Play size={40} style={{ margin: '0 auto 12px', opacity: 0.4 }} />
              <p style={{ fontSize: '14px', fontWeight: 600 }}>Henüz üretilmiş video bulunmuyor.</p>
              <p style={{ fontSize: '12px', marginTop: '4px' }}>"Anında Video Üret" butonuna tıklayarak ilk videonuzu saniyeler içinde oluşturabilirsiniz.</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {videos.slice(0, 5).map((v) => (
                <div key={v.id} style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 16px',
                  borderRadius: '12px',
                  background: 'rgba(255, 255, 255, 0.03)',
                  border: '1px solid rgba(255, 255, 255, 0.05)'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                    <div style={{
                      width: '48px',
                      height: '48px',
                      borderRadius: '8px',
                      background: '#1E293B',
                      overflow: 'hidden',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      {v.thumbnail_path ? (
                        <img src={`http://127.0.0.1:8000/${v.thumbnail_path}`} alt="Thumb" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                      ) : (
                        <Play size={20} color="#818CF8" />
                      )}
                    </div>
                    <div>
                      <h4 style={{ fontSize: '14px', fontWeight: 600, color: '#FFF' }}>{v.title}</h4>
                      <p style={{ fontSize: '12px', color: '#64748B', marginTop: '2px' }}>
                        Niş: {v.niche} • Format: {v.format?.toUpperCase()}
                      </p>
                    </div>
                  </div>

                  <span style={{
                    padding: '4px 10px',
                    borderRadius: '12px',
                    fontSize: '11px',
                    fontWeight: 700,
                    background: v.status === 'published' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(99, 102, 241, 0.15)',
                    color: v.status === 'published' ? '#34D399' : '#818CF8'
                  }}>
                    {v.status === 'published' ? 'YAYINLANDI' : 'HAZIR / KUYRUKTA'}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right Column: Channels Quick Overview */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '18px', fontWeight: 700, fontFamily: 'Outfit', color: '#FFF' }}>
              Kanal Profilleriniz
            </h3>
            <button className="btn-secondary" style={{ fontSize: '12px', padding: '6px 12px' }} onClick={() => onNavigate('channels')}>
              Yönet
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {channels.map((c) => (
              <div key={c.id} style={{
                padding: '16px',
                borderRadius: '12px',
                background: 'rgba(255, 255, 255, 0.03)',
                border: '1px solid rgba(255, 255, 255, 0.06)'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h4 style={{ fontSize: '15px', fontWeight: 700, color: '#FFF' }}>{c.name}</h4>
                  <span className="badge-autopilot">
                    {c.auto_pilot ? 'Otomatik Aktif' : 'Manuel'}
                  </span>
                </div>
                <p style={{ fontSize: '12px', color: '#94A3B8', marginTop: '6px' }}>
                  Ses: {c.voice} • Sıklık: Günde 1 Video
                </p>
              </div>
            ))}
          </div>

          <button className="btn-secondary" style={{ width: '100%', justifyContent: 'center' }} onClick={() => onNavigate('trends')}>
            <TrendingUp size={16} /> Trend Konuları Tara
          </button>
        </div>

      </div>
    </div>
  );
}
