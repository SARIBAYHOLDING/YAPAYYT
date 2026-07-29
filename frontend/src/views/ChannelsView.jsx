import React, { useState } from 'react';
import { Tv, Plus, Check, Settings, Mic, Video, ToggleLeft, ToggleRight, ExternalLink } from 'lucide-react';

export default function ChannelsView({ channels, onAddChannel, onToggleAutopilot }) {
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState('');
  const [niche, setNiche] = useState('kids_stories');
  const [voice, setVoice] = useState('tr-TR-EmelNeural');
  const [format, setFormat] = useState('shorts');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name) return;
    const newChan = {
      id: `ch_${Date.now()}`,
      name,
      niche,
      language: 'tr',
      voice,
      auto_pilot: 1,
      post_frequency: '1_per_day',
      video_format: format
    };
    onAddChannel(newChan);
    setName('');
    setShowModal(false);
  };

  return (
    <div style={{ padding: '32px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '24px', fontWeight: 800, fontFamily: 'Outfit', color: '#FFF' }}>
            Kanal Yönetimi
          </h1>
          <p style={{ color: '#94A3B8', fontSize: '14px', marginTop: '4px' }}>
            Birden fazla YouTube kanalınızı otomatik yapay zeka içerik üretimine bağlayın ve yönetin.
          </p>
        </div>

        <button className="btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={18} /> Yeni Kanal Ekle
        </button>
      </div>

      {/* Channels Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
        {channels.map((c) => (
          <div key={c.id} className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{
                  width: '48px',
                  height: '48px',
                  borderRadius: '12px',
                  background: 'linear-gradient(135deg, #6366F1 0%, #a855f7 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#FFF'
                }}>
                  <Tv size={24} />
                </div>
                <div>
                  <h3 style={{ fontSize: '18px', fontWeight: 700, fontFamily: 'Outfit', color: '#FFF' }}>{c.name}</h3>
                  <span style={{ fontSize: '12px', color: '#818CF8', fontWeight: 600 }}>{c.niche?.toUpperCase()}</span>
                </div>
              </div>

              <button 
                onClick={() => onToggleAutopilot(c.id, c.auto_pilot === 1 ? 0 : 1)}
                style={{
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  color: c.auto_pilot ? '#34D399' : '#64748B',
                  fontWeight: 600,
                  fontSize: '13px'
                }}
              >
                {c.auto_pilot ? <ToggleRight size={28} color="#34D399" /> : <ToggleLeft size={28} color="#64748B" />}
                <span>{c.auto_pilot ? 'Otomatik Otonom' : 'Devre Dışı'}</span>
              </button>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '12px',
              padding: '12px',
              borderRadius: '10px',
              background: 'rgba(0, 0, 0, 0.2)',
              fontSize: '12px',
              color: '#94A3B8'
            }}>
              <div><strong style={{ color: '#FFF' }}>Seslendirme:</strong> {c.voice}</div>
              <div><strong style={{ color: '#FFF' }}>Format:</strong> {c.video_format?.toUpperCase()}</div>
              <div><strong style={{ color: '#FFF' }}>Yayın Sıklığı:</strong> Günde 1 Video</div>
              <div><strong style={{ color: '#FFF' }}>Maliyet:</strong> 0.00 TL</div>
            </div>

            <div style={{ display: 'flex', gap: '10px', marginTop: '4px' }}>
              <button className="btn-secondary" style={{ flex: 1, justifyContent: 'center', fontSize: '13px' }}>
                <ExternalLink size={14} /> YouTube OAuth Bağla
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Add Channel Modal */}
      {showModal && (
        <div style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0, 0, 0, 0.8)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 100
        }}>
          <div className="glass-panel" style={{ width: '480px', padding: '32px' }}>
            <h3 style={{ fontSize: '20px', fontWeight: 700, color: '#FFF', marginBottom: '20px' }}>Yeni YouTube Kanalı Kur</h3>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div>
                <label style={{ fontSize: '13px', color: '#94A3B8', display: 'block', marginBottom: '6px' }}>Kanal Adı</label>
                <input className="input-field" value={name} onChange={e => setName(e.target.value)} placeholder="Örn: Masal Diyarı TV" required />
              </div>

              <div>
                <label style={{ fontSize: '13px', color: '#94A3B8', display: 'block', marginBottom: '6px' }}>İçerik Nişi</label>
                <select className="input-field" value={niche} onChange={e => setNiche(e.target.value)}>
                  <option value="kids_stories">Çocuk Hikayeleri & Masallar</option>
                  <option value="kids_learning">Çocuklar İçin Eğitici (Renkler & Hayvanlar)</option>
                  <option value="bedtime_tales">Sakinleştirici Uyku Masalları</option>
                  <option value="ai_tech_facts">Yapay Zeka & Teknoloji Gerçekleri</option>
                  <option value="facts_mysteries">İnanılmaz Bilgiler & Gizemler</option>
                </select>
              </div>

              <div>
                <label style={{ fontSize: '13px', color: '#94A3B8', display: 'block', marginBottom: '6px' }}>Seslendirme (Edge Neural Voice)</label>
                <select className="input-field" value={voice} onChange={e => setVoice(e.target.value)}>
                  <option value="tr-TR-EmelNeural">Türkçe - Emel (Kadın, Masal/Hikaye)</option>
                  <option value="tr-TR-AhmetNeural">Türkçe - Ahmet (Erkek, Enerjik/Teknoloji)</option>
                  <option value="en-US-AnaNeural">English - Ana (Cute Kids)</option>
                  <option value="en-US-ChristopherNeural">English - Christopher (Deep Male)</option>
                </select>
              </div>

              <div>
                <label style={{ fontSize: '13px', color: '#94A3B8', display: 'block', marginBottom: '6px' }}>Video Formatı</label>
                <select className="input-field" value={format} onChange={e => setFormat(e.target.value)}>
                  <option value="shorts">YouTube Shorts (9:16 Dikey 1080x1920)</option>
                  <option value="longform">Uzun Format Video (16:9 Yatay 1920x1080)</option>
                </select>
              </div>

              <div style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
                <button type="button" className="btn-secondary" style={{ flex: 1, justifyContent: 'center' }} onClick={() => setShowModal(false)}>İptal</button>
                <button type="submit" className="btn-primary" style={{ flex: 1, justifyContent: 'center' }}>Kaydet & Aktif Et</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
