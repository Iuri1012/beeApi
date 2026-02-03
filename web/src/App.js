import React, { useState, useEffect } from 'react';
import axios from 'axios';
import HiveList from './components/HiveList';
import TelemetryChart from './components/TelemetryChart';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

function App() {
  const [hives, setHives] = useState([]);
  const [selectedHive, setSelectedHive] = useState(null);
  const [telemetryData, setTelemetryData] = useState([]);
  const [ws, setWs] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');

  useEffect(() => {
    fetchHives();
  }, []);

  useEffect(() => {
    if (selectedHive) {
      fetchTelemetryHistory(selectedHive.device_id);
      connectWebSocket(selectedHive.device_id);
    }

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [selectedHive]);

  const fetchHives = async () => {
    try {
      const response = await axios.get(`${API_URL}/hives`);
      setHives(response.data);
      if (response.data.length > 0 && !selectedHive) {
        setSelectedHive(response.data[0]);
      }
    } catch (error) {
      console.error('Error fetching hives:', error);
    }
  };

  const fetchTelemetryHistory = async (deviceId) => {
    try {
      const response = await axios.get(`${API_URL}/hives/${deviceId}/telemetry?limit=50`);
      setTelemetryData(response.data.reverse());
    } catch (error) {
      console.error('Error fetching telemetry:', error);
    }
  };

  const connectWebSocket = (deviceId) => {
    if (ws) {
      ws.close();
    }

    const websocket = new WebSocket(`${WS_URL}/ws/hive/${deviceId}/telemetry`);

    websocket.onopen = () => {
      console.log('WebSocket connected');
      setConnectionStatus('connected');
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type !== 'ping') {
        console.log('Received telemetry:', data);
        setTelemetryData(prev => [...prev, data].slice(-50));
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnectionStatus('error');
    };

    websocket.onclose = () => {
      console.log('WebSocket disconnected');
      setConnectionStatus('disconnected');
    };

    setWs(websocket);
  };

  const getLatestReading = () => {
    if (telemetryData.length === 0) return null;
    return telemetryData[telemetryData.length - 1];
  };

  const latestReading = getLatestReading();

  return (
    <div className="App">
      <header className="App-header">
        <h1>🐝 BeeAPI Dashboard</h1>
        <div className={`status-indicator ${connectionStatus}`}>
          {connectionStatus === 'connected' ? '● Live' : connectionStatus === 'error' ? '● Error' : '○ Offline'}
        </div>
      </header>
      
      <div className="container">
        <div className="sidebar">
          <h2>Hives</h2>
          <HiveList 
            hives={hives} 
            selectedHive={selectedHive}
            onSelectHive={setSelectedHive}
          />
        </div>

        <div className="main-content">
          {selectedHive ? (
            <>
              <div className="hive-header">
                <h2>{selectedHive.name || selectedHive.device_id}</h2>
                <p className="location">{selectedHive.location || 'Unknown location'}</p>
              </div>

              {latestReading && (
                <div className="metrics-grid">
                  <div className="metric-card">
                    <div className="metric-icon">🌡️</div>
                    <div className="metric-value">{latestReading.temperature?.toFixed(1) || 'N/A'}°C</div>
                    <div className="metric-label">Temperature</div>
                  </div>
                  <div className="metric-card">
                    <div className="metric-icon">💧</div>
                    <div className="metric-value">{latestReading.humidity?.toFixed(1) || 'N/A'}%</div>
                    <div className="metric-label">Humidity</div>
                  </div>
                  <div className="metric-card">
                    <div className="metric-icon">⚖️</div>
                    <div className="metric-value">{latestReading.weight?.toFixed(1) || 'N/A'} kg</div>
                    <div className="metric-label">Weight</div>
                  </div>
                  <div className="metric-card">
                    <div className="metric-icon">🔊</div>
                    <div className="metric-value">{latestReading.sound_level?.toFixed(1) || 'N/A'} dB</div>
                    <div className="metric-label">Sound Level</div>
                  </div>
                </div>
              )}

              <div className="charts">
                <TelemetryChart data={telemetryData} />
              </div>
            </>
          ) : (
            <div className="no-data">
              <p>No hives registered. Please register a device first.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
