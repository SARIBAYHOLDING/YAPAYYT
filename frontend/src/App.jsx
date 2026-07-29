import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import DashboardView from './views/DashboardView';
import ChannelsView from './views/ChannelsView';
import GeneratorView from './views/GeneratorView';
import TrendsView from './views/TrendsView';
import StudioView from './views/StudioView';
import SettingsView from './views/SettingsView';
import axios from 'axios';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [channels, setChannels] = useState([
    {
      id: 'ch_kids_main',
      name: 'Sevimli Masal Dünyası',
      niche: 'kids_stories',
      language: 'tr',
      voice: 'tr-TR-EmelNeural',
      auto_pilot: 1,
      post_frequency: '1_per_day',
      video_format: 'shorts'
    },
    {
      id: 'ch_tech_main',
      name: 'AI Teknoloji Rehberi',
      niche: 'ai_tech_facts',
      language: 'tr',
      voice: 'tr-TR-AhmetNeural',
      auto_pilot: 0,
      post_frequency: '1_per_day',
      video_format: 'shorts'
    }
  ]);

  const [videos, setVideos] = useState([]);

  // Fetch backend data
  const loadData = async () => {
    try {
      const chanRes = await axios.get('http://127.0.0.1:8000/api/channels');
      if (chanRes.data && chanRes.data.length > 0) {
        setChannels(chanRes.data);
      }
      const vidRes = await axios.get('http://127.0.0.1:8000/api/videos');
      if (vidRes.data) {
        setVideos(vidRes.data);
      }
    } catch (e) {
      console.log('Connecting to local backend API...');
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAddChannel = async (newChannel) => {
    setChannels([newChannel, ...channels]);
    try {
      await axios.post('http://127.0.0.1:8000/api/channels', newChannel);
    } catch (e) {
      console.error(e);
    }
  };

  const handleToggleAutopilot = async (channelId, status) => {
    setChannels(channels.map(c => c.id === channelId ? { ...c, auto_pilot: status } : c));
    try {
      await axios.put(`http://127.0.0.1:8000/api/channels/${channelId}/autopilot?auto_pilot=${status}`);
    } catch (e) {
      console.error(e);
    }
  };

  const handleGenerateVideo = async (payload) => {
    const res = await axios.post('http://127.0.0.1:8000/api/videos/generate', payload);
    await loadData();
    return res.data;
  };

  const handleDeleteVideo = async (videoId) => {
    setVideos(videos.filter(v => v.id !== videoId));
    try {
      await axios.delete(`http://127.0.0.1:8000/api/videos/${videoId}`);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#07090E' }}>
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main style={{ marginLeft: '260px', flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Header activeChannelsCount={channels.length} totalVideosCount={videos.length} />
        
        {activeTab === 'dashboard' && (
          <DashboardView channels={channels} videos={videos} onNavigate={setActiveTab} />
        )}

        {activeTab === 'channels' && (
          <ChannelsView 
            channels={channels} 
            onAddChannel={handleAddChannel} 
            onToggleAutopilot={handleToggleAutopilot} 
          />
        )}

        {activeTab === 'generator' && (
          <GeneratorView channels={channels} onGenerateVideo={handleGenerateVideo} />
        )}

        {activeTab === 'trends' && (
          <TrendsView onSelectTrendForGeneration={(trendTopic) => {
            setActiveTab('generator');
          }} />
        )}

        {activeTab === 'studio' && (
          <StudioView videos={videos} onDeleteVideo={handleDeleteVideo} />
        )}

        {activeTab === 'settings' && (
          <SettingsView />
        )}
      </main>
    </div>
  );
}
