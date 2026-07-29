import React from 'react';
import { 
  LayoutDashboard, 
  Tv, 
  Sparkles, 
  TrendingUp, 
  Film, 
  Settings, 
  Bot,
  Zap,
  Play
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'dashboard', label: 'Genel Bakış', icon: LayoutDashboard },
    { id: 'generator', label: 'Hızlı Video Üretici', icon: Sparkles, highlight: true },
    { id: 'channels', label: 'Kanal Yönetimi', icon: Tv },
    { id: 'studio_hub', label: 'YouTube Studio Hub', icon: Play, highlight: false },
    { id: 'trends', label: 'Trend & Esinlenme', icon: TrendingUp },
    { id: 'studio', label: 'Video & Önizleme Stüdyosu', icon: Film },
    { id: 'settings', label: 'Sistem Ayarları', icon: Settings },
  ];

  return (
    <aside style={{
      width: '260px',
      height: '100vh',
      position: 'fixed',
      left: 0,
      top: 0,
      backgroundColor: '#0A0E17',
      borderRight: '1px solid rgba(255, 255, 255, 0.08)',
      display: 'flex',
      flexDirection: 'column',
      padding: '24px 16px',
      zIndex: 50
    }}>
      {/* Brand & Logo Header */}
      <div style={{ marginBottom: '32px', paddingLeft: '8px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #6366F1 0%, #a855f7 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#FFF',
            boxShadow: '0 4px 15px rgba(99, 102, 241, 0.4)'
          }}>
            <Bot size={24} />
          </div>
          <div>
            <h1 style={{ fontSize: '18px', fontWeight: 800, fontFamily: 'Outfit', color: '#FFF', letterSpacing: '-0.5px' }}>
              SARIBAY <span style={{ color: '#818CF8' }}>AI TUBE</span>
            </h1>
            <p style={{ fontSize: '11px', color: '#64748B', fontWeight: 600 }}>Sarıbay Yazılım v2.5</p>
          </div>
        </div>
      </div>

      {/* Zero Cost Badge */}
      <div style={{
        marginBottom: '24px',
        padding: '12px',
        borderRadius: '12px',
        background: 'rgba(16, 185, 129, 0.08)',
        border: '1px solid rgba(52, 211, 153, 0.2)',
        display: 'flex',
        alignItems: 'center',
        gap: '10px'
      }}>
        <Zap size={18} color="#34D399" />
        <div>
          <div style={{ fontSize: '12px', fontWeight: 700, color: '#34D399' }}>%100 SIFIR MALİYET</div>
          <div style={{ fontSize: '10px', color: '#94A3B8' }}>Ücretsiz AI & Neural Speech</div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                borderRadius: '12px',
                border: 'none',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: isActive ? 700 : 500,
                color: isActive ? '#FFFFFF' : '#94A3B8',
                background: isActive 
                  ? (item.highlight ? 'linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(168, 85, 247, 0.3) 100%)' : 'rgba(255, 255, 255, 0.08)')
                  : 'transparent',
                borderLeft: isActive ? '3px solid #6366F1' : '3px solid transparent',
                transition: 'all 0.2s ease',
                textAlign: 'left'
              }}
            >
              <Icon size={20} color={isActive ? '#818CF8' : '#64748B'} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Footer Branding */}
      <div style={{ 
        paddingTop: '16px', 
        borderTop: '1px solid rgba(255, 255, 255, 0.08)',
        fontSize: '11px',
        color: '#64748B',
        textAlign: 'center'
      }}>
        Geliştirici: <strong style={{ color: '#CBD5E1' }}>Selahattin Sarıbay</strong>
      </div>
    </aside>
  );
}
