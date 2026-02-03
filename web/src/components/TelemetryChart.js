import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './TelemetryChart.css';

function TelemetryChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="no-chart-data">
        <p>No telemetry data available</p>
      </div>
    );
  }

  const chartData = data.map(item => ({
    time: new Date(item.time).toLocaleTimeString(),
    temperature: item.temperature,
    humidity: item.humidity,
    weight: item.weight,
    sound_level: item.sound_level,
  }));

  return (
    <div className="telemetry-chart">
      <h3>Live Telemetry</h3>
      
      <div className="chart-container">
        <h4>Temperature & Humidity</h4>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="temperature" stroke="#ff6b6b" name="Temperature (°C)" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="humidity" stroke="#4ecdc4" name="Humidity (%)" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-container">
        <h4>Weight</h4>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="weight" stroke="#95e1d3" name="Weight (kg)" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-container">
        <h4>Sound Level</h4>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="sound_level" stroke="#ffd93d" name="Sound Level (dB)" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default TelemetryChart;
