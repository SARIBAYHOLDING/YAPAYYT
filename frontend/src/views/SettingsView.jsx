import React, { useState } from 'react';
import { Settings, Key, ShieldCheck, Cpu, Code } from 'lucide-react';

export default function SettingsView() {
  const [geminiKey, setGeminiKey] = useState('');
  const [saved, setSaved] = useState(false);

  const handleSave = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div style={{ padding: '32px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '24px', fontWeight: 800, fontFamily: 'Outfit', color: '#FFF' }}>
          Sistem Ayarları & Yapılandırma
        </h1>
        <p style={{ color: '#94A3B8', fontSize: '14px', marginTop: '4px' }}>
          Google AI / Gemini API anahtarlarınızı girin ve sıfır maliyet motoru tercihlerini yönetin.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        
        <div className="glass-panel" style={{ padding: '32px' }}>
          <form onSubmit={handleSave} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div>
              <label style={{ fontSize: '14px', fontWeight: 600, color: '#FFF', display: 'block', marginBottom: '8px' }}>
                Google Gemini API Key (İsteğe Bağlı)
              </label>
              <input 
                className="input-field" 
                type="password"
                value={geminiKey}
                onChange={e => setGeminiKey(e.target.value)}
                placeholder="AIzaSy... (Boş bırakılırsa dahili şablon motoru çalışır)"
              />
              <span style={{ fontSize: '12px', color: '#64748B', display: 'block', marginTop: '6px' }}>
                Google AI Pro / Gemini Flash ücretsiz tier anahtarınızı ekleyerek daha derin ve özel senaryolar üretebilirsiniz.
              </span>
            </div>

            <button type="submit" className="btn-primary">
              Ayarları Kaydet
            </button>

            {saved && (
              <div style={{ color: '#34D399', fontSize: '13px', fontWeight: 600 }}>
                ✓ Ayarlar başarıyla güncellendi!
              </div>
            )}
          </form>
        </div>

        {/* System Info Box */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#FFF' }}>Sistem Mimarisi</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px', color: '#94A3B8' }}>
            <div><strong style={{ color: '#FFF' }}>Yazılım:</strong> Sarıbay AI YouTube Automation Studio</div>
            <div><strong style={{ color: '#FFF' }}>Geliştirici:</strong> Selahattin Sarıbay</div>
            <div><strong style={{ color: '#FFF' }}>Firma:</strong> Sarıbay Yazılım</div>
            <div><strong style={{ color: '#FFF' }}>Ses Motoru:</strong> Edge-TTS (Neural)</div>
            <div><strong style={{ color: '#FFF' }}>Görsel Motoru:</strong> Pollinations AI (Flux)</div>
            <div><strong style={{ color: '#FFF' }}>Render Motoru:</strong> FFmpeg + MoviePy</div>
          </div>
        </div>

      </div>
    </div>
  );
}
