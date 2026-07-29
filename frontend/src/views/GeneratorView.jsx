import React, { useState } from 'react';
import { Sparkles, Play, CheckCircle2, Loader2, Wand2, Film, ShieldCheck, Layers, Flame, BarChart } from 'lucide-react';
import axios from 'axios';

export default function GeneratorView({ channels, onGenerateVideo }) {
  const [selectedChannel, setSelectedChannel] = useState(channels[0]?.id || '');
  const [topic, setTopic] = useState('');
  const [isBatch, setIsBatch] = useState(false);
  const [batchTopics, setBatchTopics] = useState('');
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

  const [progressPercent, setProgressPercent] = useState(0);

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!selectedChannel) return;

    setIsGenerating(true);
    setProgressPercent(5);
    setCurrentStep('Başlatılıyor...');
    setResultMessage('');

    try {
      if (isBatch) {
        const topicsList = batchTopics.split('\n').map(t => t.trim()).filter(Boolean);
        if (topicsList.length === 0) {
          setIsGenerating(false);
          return;
        }
        setCurrentStep(`Toplu Üretim Başlatıldı (${topicsList.length} Video)...`);
        await axios.post('http://127.0.0.1:8000/api/videos/batch-generate', {
          channel_id: selectedChannel,
          topics: topicsList
        });
        setProgressPercent(100);
        setResultMessage(`🎉 Tebrikler! ${topicsList.length} Adet Video Başarıyla Üretildi!`);
      } else {
        if (!topic) return;
        const res = await onGenerateVideo({
          channel_id: selectedChannel,
          topic: topic
        });

        const jobId = res.job_id;
        if (jobId) {
          // Poll real-time progress from backend
          const pollInterval = setInterval(async () => {
            try {
              const progRes = await axios.get(`http://127.0.0.1:8000/api/videos/progress/${jobId}`);
              const prog = progRes.data;
              if (prog) {
                setProgressPercent(prog.progress_percent || 10);
                setCurrentStep(prog.current_step || 'Üretim devam ediyor...');
                if (prog.status === 'completed' || prog.progress_percent >= 100) {
                  clearInterval(pollInterval);
                  setIsGenerating(false);
                  setResultMessage('🎉 Harika! Video, Seslendirme, Müzik & Kapak Görseli Tamamlandı!');
                } else if (prog.status === 'failed') {
                  clearInterval(pollInterval);
                  setIsGenerating(false);
                  setResultMessage('Hata oluştu: ' + (prog.error || 'Üretim başarısız'));
                }
              }
            } catch (e) {
              console.error(e);
            }
          }, 1500);
        } else {
          setIsGenerating(false);
          setResultMessage('🎉 Video Başarıyla Üretildi.');
        }
      }
    } catch (err) {
      setIsGenerating(false);
      setResultMessage('Hata oluştu: ' + (err.message || 'Üretim tamamlanamadı.'));
    }
  };

  return (
    <div style={{ padding: '32px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '24px', fontWeight: 800, fontFamily: 'Outfit', color: '#FFF' }}>
            Ultra HD Kaliteli Video Üretici 🎬
          </h1>
          <p style={{ color: '#94A3B8', fontSize: '14px', marginTop: '4px' }}>
            Yüksek çözünürlüklü HD klipler, AI görseller, arka plan müzikleri ve sinematik Ken Burns efektiyle ultra kaliteli videolar üretin.
          </p>
        </div>

        {/* Mode Toggle: Single vs Batch */}
        <div style={{ display: 'flex', gap: '8px', background: 'rgba(255, 255, 255, 0.05)', padding: '4px', borderRadius: '12px' }}>
          <button 
            type="button"
            onClick={() => setIsBatch(false)}
            style={{
              padding: '8px 16px',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '13px',
              background: !isBatch ? '#6366F1' : 'transparent',
              color: '#FFF'
            }}
          >
            Tekil Video Üretimi
          </button>
          <button 
            type="button"
            onClick={() => setIsBatch(true)}
            style={{
              padding: '8px 16px',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '13px',
              background: isBatch ? '#6366F1' : 'transparent',
              color: '#FFF',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <Layers size={16} /> Toplu (Batch) Üretim
          </button>
        </div>
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

            {!isBatch ? (
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
                  required={!isBatch}
                />
              </div>
            ) : (
              <div>
                <label style={{ fontSize: '14px', fontWeight: 600, color: '#FFF', display: 'block', marginBottom: '8px' }}>
                  Toplu Video Konuları (Her Satıra Bir Konu Yazın)
                </label>
                <textarea 
                  className="input-field"
                  style={{ fontSize: '14px', padding: '14px', minHeight: '140px', resize: 'vertical' }}
                  value={batchTopics}
                  onChange={e => setBatchTopics(e.target.value)}
                  placeholder={"Sihirli Ormanın Kayıp Yıldızı\nKüçük Dinazor Dino\n2030 Yapay Zeka Devrimi\nUzay Trenleri Macerası"}
                  required={isBatch}
                />
              </div>
            )}

            {/* Topic Ideas */}
            {!isBatch && (
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
            )}

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
                    <span>10x Üretim İşleniyor...</span>
                  </>
                ) : (
                  <>
                    <Wand2 size={20} />
                    <span>{isBatch ? 'Toplu (Batch) Üretimi Başlat' : '10x İyileştirilmiş Üretimi Başlat (0 TL)'}</span>
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Realtime Animated Progress Bar */}
          {isGenerating && (
            <div style={{
              marginTop: '24px',
              padding: '24px',
              borderRadius: '16px',
              background: 'rgba(99, 102, 241, 0.1)',
              border: '1px solid rgba(99, 102, 241, 0.3)',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '14px', fontWeight: 700, color: '#FFF' }}>{currentStep}</span>
                <span style={{ fontSize: '16px', fontWeight: 800, color: '#818CF8', fontFamily: 'Outfit' }}>%{progressPercent}</span>
              </div>
              <div style={{ width: '100%', height: '12px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '6px', overflow: 'hidden' }}>
                <div style={{
                  width: `${progressPercent}%`,
                  height: '100%',
                  background: 'linear-gradient(90deg, #6366F1 0%, #a855f7 50%, #ec4899 100%)',
                  borderRadius: '6px',
                  boxShadow: '0 0 15px rgba(99, 102, 241, 0.8)',
                  transition: 'width 0.5s cubic-bezier(0.4, 0, 0.2, 1)'
                }} />
              </div>
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
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#FFF', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Flame size={18} color="#EF4444" /> 10x İyileştirme Özellikleri
          </h3>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px', color: '#94A3B8' }}>
            <li style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <CheckCircle2 size={16} color="#34D399" /> İlk 3 Saniyede Viral Kanca (Hook)
            </li>
            <li style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <CheckCircle2 size={16} color="#34D399" /> Arka Plan Müzikleri & SFX Miksi
            </li>
            <li style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <CheckCircle2 size={16} color="#34D399" /> HD Gerçek Klipler + AI Görseller
            </li>
            <li style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <CheckCircle2 size={16} color="#34D399" /> Toplu (Batch) Video Üretim Motoru
            </li>
            <li style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <CheckCircle2 size={16} color="#34D399" /> Yüksek CTR Kapak Görseli
            </li>
          </ul>
        </div>

      </div>
    </div>
  );
}
