import React, { useState } from 'react';
import { Sparkles, Play, CheckCircle2, Loader2, Wand2, Film, ShieldCheck } from 'lucide-react';

export default function GeneratorView({ channels, onGenerateVideo }) {
  const [selectedChannel, setSelectedChannel] = useState(channels[0]?.id || '');
  const [topic, setTopic] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentStep, setCurrentStep] = useState('');
  const [resultMessage, setResultMessage] = useState('');

  const sampleTopics = [
    "Pamuk Kuyruklu Sevimli Tavşanın Sihirli Bahçesi",
    "Uzay Yolcusu Leo ve Kayıp Yıldız Masalı",
    "2030 Yılında İnsanlığı Şaşırtacak 5 Yapay Zeka Gelişmesi",
    "Okyanus Altındaki Rengarenk Balık Boncuk",
    "Küçük Ejderha Kuki ve Dostluk Ormanı"
  ];

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!topic || !selectedChannel) return;

    setIsGenerating(true);
    setCurrentStep('1/5 - Gemini AI ile Senaryo ve Sahne Detayları Hazırlanıyor...');
    setResultMessage('');

    try {
      setTimeout(() => setCurrentStep('2/5 - Edge Neural Speech ile Doğal Türkçe Seslendirme Oluşturuluyor...'), 2000);
      setTimeout(() => setCurrentStep('3/5 - Pollinations AI ile 1080p Sahne Görselleri Üretiliyor...'), 5000);
      setTimeout(() => setCurrentStep('4/5 - FFmpeg ve Alt Yazı Motoru ile Video İşleniyor (Render)...'), 8000);
      setTimeout(() => setCurrentStep('5/5 - Yüksek CTR Kapak Görseli (Thumbnail) Tasarlanıyor...'), 11000);

      const res = await onGenerateVideo({
        channel_id: selectedChannel,
        topic: topic
      });

      setResultMessage('🎉 Harika! Video ve Kapak Görseli Başarıyla Üretildi.');
    } catch (err) {
      setResultMessage('Hata oluştu: ' + (err.message || 'Üretim tamamlanamadı.'));
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div style={{ padding: '32px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '24px', fontWeight: 800, fontFamily: 'Outfit', color: '#FFF' }}>
          Hızlı Video Üretici
        </h1>
        <p style={{ color: '#94A3B8', fontSize: '14px', marginTop: '4px' }}>
          Konuyu yazın veya bir fikir seçin; sistem senaryoyu yazar, seslendirir, AI görselleri çizer ve 1080p MP4 videoyu hazırlar.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        
        {/* Main Generator Form */}
        <div className="glass-panel" style={{ padding: '32px' }}>
          <form onSubmit={handleGenerate} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            
            <div>
              <label style={{ fontSize: '14px', fontWeight: 600, color: '#FFF', display: 'block', marginBottom: '8px' }}>
                Hangi Kanal İçin Üretilecek?
              </label>
              <select className="input-field" value={selectedChannel} onChange={e => setSelectedChannel(e.target.value)}>
                {channels.map(c => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.niche?.toUpperCase()})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ fontSize: '14px', fontWeight: 600, color: '#FFF', display: 'block', marginBottom: '8px' }}>
                Video Konusu veya Anahtar Kelime
              </label>
              <input 
                className="input-field"
                style={{ fontSize: '16px', padding: '16px' }}
                value={topic}
                onChange={e => setTopic(e.target.value)}
                placeholder="Örn: Pamuk Tavşanın Orman Maceraları veya Geleceğin Robotları..."
                required
              />
            </div>

            {/* Topic Ideas */}
            <div>
              <span style={{ fontSize: '12px', color: '#64748B', display: 'block', marginBottom: '8px' }}>
                💡 Hızlı Fikirler (Tıklayıp Deneyin):
              </span>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {sampleTopics.map((t, idx) => (
                  <button 
                    key={idx}
                    type="button"
                    onClick={() => setTopic(t)}
                    style={{
                      background: 'rgba(255, 255, 255, 0.04)',
                      border: '1px solid rgba(255, 255, 255, 0.08)',
                      borderRadius: '20px',
                      padding: '6px 14px',
                      fontSize: '12px',
                      color: '#CBD5E1',
                      cursor: 'pointer'
                    }}
                  >
                    + {t}
                  </button>
                ))}
              </div>
            </div>

            <div style={{ marginTop: '12px' }}>
              <button 
                type="submit" 
                className="btn-primary" 
                disabled={isGenerating}
                style={{ width: '100%', justifyContent: 'center', padding: '16px', fontSize: '16px' }}
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    <span>Üretim Devam Ediyor...</span>
                  </>
                ) : (
                  <>
                    <Wand2 size={20} />
                    <span>Tam Otomatik Üretimi Başlat (0 TL)</span>
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Realtime Progress Steps */}
          {isGenerating && (
            <div style={{
              marginTop: '24px',
              padding: '20px',
              borderRadius: '12px',
              background: 'rgba(99, 102, 241, 0.1)',
              border: '1px solid rgba(99, 102, 241, 0.3)',
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              color: '#818CF8',
              fontSize: '14px',
              fontWeight: 600
            }}>
              <Loader2 size={24} style={{ animation: 'spin 1.5s linear infinite' }} />
              <div>{currentStep}</div>
            </div>
          )}

          {resultMessage && (
            <div style={{
              marginTop: '24px',
              padding: '20px',
              borderRadius: '12px',
              background: 'rgba(16, 185, 129, 0.15)',
              border: '1px solid rgba(52, 211, 153, 0.3)',
              color: '#34D399',
              fontSize: '14px',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '10px'
            }}>
              <CheckCircle2 size={20} />
              <div>{resultMessage}</div>
            </div>
          )}
        </div>

        {/* Right Help Column */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#FFF' }}>Neler Otomatik Yapılır?</h3>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px', color: '#94A3B8' }}>
            <li style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <CheckCircle2 size={16} color="#34D399" /> Google Gemini ile SEO Uyumlu Başlık ve Açıklama
            </li>
            <li style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <CheckCircle2 size={16} color="#34D399" /> Microsoft Edge Neural TTS ile Türkçe Seslendirme
            </li>
            <li style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <CheckCircle2 size={16} color="#34D399" /> Pollinations AI ile HD Sahne Çizimleri
            </li>
            <li style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <CheckCircle2 size={16} color="#34D399" /> FFmpeg Ken Burns Zoom ve Sarı Alt Yazılar
            </li>
            <li style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <CheckCircle2 size={16} color="#34D399" /> Tıklama Odaklı YouTube Kapak Görseli
            </li>
          </ul>
        </div>

      </div>
    </div>
  );
}
