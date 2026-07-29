import React from 'react';
import { Activity, Play, ShieldCheck, CheckCircle2 } from 'lucide-react';

export default function Header({ systemHealth, activeChannelsCount, totalVideosCount }) {
  return (
    <header style={{
      height: '70px',
      borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 32px',
      backgroundColor: 'rgba(10, 14, 23, 0.6)',
      backdropFilter: 'blur(12px)',
      position: 'sticky',
      top: 0,
      zIndex: 40
    }}>
      {/* Page / System Title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <h2 style={{ fontSize: '18px', fontWeight: 700, fontFamily: 'Outfit', color: '#FFF' }}>
          YouTube Otomasyon Kontrol Stüdyosu
        </h2>
        <span className="badge-zero-cost">
          <ShieldCheck size={14} /> 0 TL Sıfır Maliyet Aktif
        </span>
      </div>

      {/* System Status Indicators */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', color: '#94A3B8' }}>
          <Activity size={16} color="#10B981" />
          <span>Kanal Sayısı: <strong style={{ color: '#FFF' }}>{activeChannelsCount || 2}</strong></span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', color: '#94A3B8' }}>
          <Play size={16} color="#818CF8" />
          <span>Üretilen Videolar: <strong style={{ color: '#FFF' }}>{totalVideosCount || 0}</strong></span>
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          padding: '6px 14px',
          borderRadius: '20px',
          background: 'rgba(16, 185, 129, 0.1)',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          color: '#34D399',
          fontSize: '12px',
          fontWeight: 600
        }}>
          <CheckCircle2 size={14} /> Otomatik Mod Hazır
        </div>
      </div>
    </header>
  );
}
