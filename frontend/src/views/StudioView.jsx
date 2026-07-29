import React, { useState } from 'react';
import { Play, Download, Trash2, Film, CheckCircle2, FileText, Image as ImageIcon, Volume2, ExternalLink, Copy, Tv } from 'lucide-react';

export default function StudioView({ videos, onDeleteVideo }) {
  const [selectedVideo, setSelectedVideo] = useState(videos[0] || null);
  const [copiedLink, setCopiedLink] = useState(false);

  const activeYoutubeUrl = selectedVideo?.youtube_url || (selectedVideo ? `https://www.youtube.com/watch?v=${selectedVideo.id}` : '');

  const handleCopyLink = () => {
    if (activeYoutubeUrl) {
      navigator.clipboard.writeText(activeYoutubeUrl);
      setCopiedLink(true);
      setTimeout(() => setCopiedLink(false), 2000);
    }
  };

  return (
    <div style={{ padding: '32px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '24px', fontWeight: 800, fontFamily: 'Outfit', color: '#FFF' }}>
          Video & Önizleme Stüdyosu 🎬
        </h1>
        <p style={{ color: '#94A3B8', fontSize: '14px', marginTop: '4px' }}>
          Üretilen tüm videolarınızı sahne sahne inceleyin, 1080p önizlemesini izleyin ve doğrudan YouTube bağlantısını görüntüleyin.
        </p>
      </div>

      {videos.length === 0 ? (
        <div className="glass-panel" style={{ padding: '60px', textAlign: 'center', color: '#64748B' }}>
          <Film size={48} style={{ margin: '0 auto 16px', opacity: 0.4 }} />
          <h3 style={{ color: '#FFF', fontSize: '18px' }}>Stüdyoda Henüz Video Yok</h3>
          <p style={{ marginTop: '8px', fontSize: '14px' }}>Hızlı Video Üretici'den yeni bir video oluşturarak stüdyoya ekleyebilirsiniz.</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '24px' }}>
          
          {/* Left: Video List */}
          <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '75vh', overflowY: 'auto' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#FFF', marginBottom: '8px' }}>Üretilen İçerikler</h3>
            {videos.map((v) => (
              <div 
                key={v.id}
                onClick={() => setSelectedVideo(v)}
                style={{
                  padding: '12px',
                  borderRadius: '10px',
                  background: selectedVideo?.id === v.id ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                  border: selectedVideo?.id === v.id ? '1px solid #6366F1' : '1px solid rgba(255, 255, 255, 0.06)',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px'
                }}
              >
                <div style={{ width: '40px', height: '40px', borderRadius: '6px', background: '#1E293B', overflow: 'hidden' }}>
                  {v.thumbnail_path ? (
                    <img src={`http://127.0.0.1:8000/${v.thumbnail_path}`} alt="Thumb" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                  ) : (
                    <Film size={20} color="#818CF8" />
                  )}
                </div>
                <div style={{ flex: 1, overflow: 'hidden' }}>
                  <h4 style={{ fontSize: '13px', fontWeight: 600, color: '#FFF', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {v.title}
                  </h4>
                  <span style={{ fontSize: '11px', color: '#94A3B8' }}>{v.format?.toUpperCase()}</span>
                </div>
              </div>
            ))}
          </div>

          {/* Right: Selected Video Details & Media Player */}
          {selectedVideo && (
            <div className="glass-panel" style={{ padding: '28px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <h2 style={{ fontSize: '20px', fontWeight: 700, fontFamily: 'Outfit', color: '#FFF' }}>
                    {selectedVideo.title}
                  </h2>
                  <p style={{ color: '#94A3B8', fontSize: '13px', marginTop: '4px' }}>
                    Niş: {selectedVideo.niche} • Format: {selectedVideo.format?.toUpperCase()}
                  </p>
                </div>

                <button 
                  onClick={() => onDeleteVideo(selectedVideo.id)}
                  style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', color: '#EF4444', padding: '8px', borderRadius: '8px', cursor: 'pointer' }}
                >
                  <Trash2 size={18} />
                </button>
              </div>

              {/* Prominent YouTube Video Link Container */}
              <div style={{
                padding: '16px 20px',
                borderRadius: '12px',
                background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(15, 23, 42, 0.6) 100%)',
                border: '1px solid rgba(239, 68, 68, 0.4)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                gap: '16px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', overflow: 'hidden' }}>
                  <Tv size={24} color="#EF4444" />
                  <div style={{ overflow: 'hidden' }}>
                    <span style={{ fontSize: '11px', fontWeight: 700, color: '#EF4444', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                      YouTube Video Bağlantısı
                    </span>
                    <div style={{ fontSize: '13px', color: '#FFF', fontWeight: 600, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {activeYoutubeUrl}
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '8px' }}>
                  <button 
                    onClick={handleCopyLink}
                    className="btn-secondary"
                    style={{ fontSize: '12px', padding: '8px 14px', whiteSpace: 'nowrap' }}
                  >
                    <Copy size={14} /> {copiedLink ? 'Kopyalandı!' : 'Kopyala'}
                  </button>

                  <a 
                    href={activeYoutubeUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="btn-primary"
                    style={{ fontSize: '12px', padding: '8px 16px', background: 'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)', boxShadow: '0 4px 15px rgba(239, 68, 68, 0.4)', whiteSpace: 'nowrap' }}
                  >
                    <ExternalLink size={14} /> YouTube'da İzle 📺
                  </a>
                </div>
              </div>

              {/* Video Player */}
              <div style={{
                width: '100%',
                maxHeight: '400px',
                borderRadius: '12px',
                overflow: 'hidden',
                background: '#000',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                {selectedVideo.video_path ? (
                  <video 
                    controls 
                    style={{ maxHeight: '400px', width: 'auto', borderRadius: '12px' }}
                    src={`http://127.0.0.1:8000/${selectedVideo.video_path}`}
                  />
                ) : (
                  <div style={{ color: '#64748B', padding: '40px' }}>Video dosyası yükleniyor...</div>
                )}
              </div>

              {/* Scene Breakdown */}
              <div>
                <h4 style={{ fontSize: '15px', fontWeight: 700, color: '#FFF', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <FileText size={18} color="#818CF8" /> Senaryo & Sahne Dökümü
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {selectedVideo.script_data?.scenes?.map((s, idx) => (
                    <div key={idx} style={{
                      padding: '12px 16px',
                      borderRadius: '10px',
                      background: 'rgba(255, 255, 255, 0.03)',
                      fontSize: '13px',
                      color: '#CBD5E1',
                      lineHeight: '1.5'
                    }}>
                      <strong style={{ color: '#818CF8' }}>Sahne {s.scene_num}:</strong> {s.narration}
                    </div>
                  ))}
                </div>
              </div>

            </div>
          )}

        </div>
      )}
    </div>
  );
}
