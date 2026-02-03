# BeeAPI Web Dashboard UI

## Overview

The BeeAPI web dashboard provides real-time monitoring of beehive telemetry data through an intuitive React-based interface.

## Main Dashboard View

### Header
```
┌────────────────────────────────────────────────────────────────┐
│  🐝 BeeAPI Dashboard                              ● Live       │
└────────────────────────────────────────────────────────────────┘
```

### Layout

**Sidebar - Hive List:**
```
┌──────────────┐
│   Hives      │
├──────────────┤
│ 🐝 hive-001  │ ← Selected (highlighted)
│ Test Hive    │
│ Apiary A     │
├──────────────┤
│ 🐝 hive-002  │
│ Alpha Hive   │
│ Apiary B     │
└──────────────┘
```

**Main Content - Telemetry Display:**

**Hive Header:**
```
┌────────────────────────────────────────────┐
│  Test Hive Alpha                           │
│  📍 Apiary A                               │
└────────────────────────────────────────────┘
```

**Live Metrics Cards:**
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  🌡️          │ │  💧          │ │  ⚖️          │ │  🔊          │
│   35.5°C     │ │   62.3%      │ │  45.2 kg     │ │  48.7 dB     │
│ Temperature  │ │  Humidity    │ │   Weight     │ │ Sound Level  │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Real-Time Charts:**
```
┌────────────────────────────────────────────────────────────────┐
│  Live Telemetry                                                │
├────────────────────────────────────────────────────────────────┤
│  Temperature & Humidity                                        │
│                                                                │
│  40°C ┤                     ╱╲                                │
│       │                   ╱    ╲      ╱╲                      │
│  35°C ┤              ╱╲  ╱      ╲    ╱  ╲    Temperature     │
│       │            ╱    ╲╱        ╲╱      ╲                   │
│  30°C ┼─────────────────────────────────────────────          │
│                                                                │
│  70%  ┤        ╱╲      ╱╲                                     │
│  65%  ┤      ╱    ╲  ╱    ╲    ╱╲         Humidity           │
│  60%  ┤    ╱      ╲╱      ╲  ╱  ╲                            │
│  55%  ┼─────────────────────────────────────────────          │
│       └─────────────────────────────────────────────          │
│         13:00   13:15   13:30   13:45   14:00                 │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  Weight                                                        │
│                                                                │
│  46kg ┤                                                        │
│  45kg ┤    ────────────────────────────────────               │
│  44kg ┤                                                        │
│       └─────────────────────────────────────────────          │
│         13:00   13:15   13:30   13:45   14:00                 │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  Sound Level                                                   │
│                                                                │
│  60dB ┤        ╱╲                      ╱╲                     │
│  50dB ┤    ╱╲╱  ╲╱╲                  ╱  ╲                    │
│  40dB ┤  ╱          ╲──────────────╱      ╲                   │
│       └─────────────────────────────────────────────          │
│         13:00   13:15   13:30   13:45   14:00                 │
└────────────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Real-Time Updates
- WebSocket connection provides live telemetry updates
- Green "● Live" indicator shows active connection
- Updates every 5 seconds as simulator publishes data

### 2. Multiple Hive Support
- Sidebar lists all registered hives
- Click any hive to view its telemetry
- Each hive has unique identifier, name, and location

### 3. Metric Cards
- Large, easy-to-read current values
- Color-coded icons for each metric type
- Hover effects for interactivity

### 4. Interactive Charts
- Time-series visualization using Recharts
- Separate charts for related metrics
- Tooltip displays exact values on hover
- Responsive design adapts to screen size

### 5. Connection Status
- Live indicator shows WebSocket status:
  - 🟢 "● Live" - Connected and receiving data
  - 🔴 "● Error" - Connection error
  - ⚪ "○ Offline" - Disconnected

## Color Scheme

- **Primary**: Purple gradient (`#667eea` to `#764ba2`)
- **Background**: Light gray (`#f5f7fa`)
- **Cards**: White with subtle shadow
- **Charts**:
  - Temperature: Red (`#ff6b6b`)
  - Humidity: Teal (`#4ecdc4`)
  - Weight: Mint green (`#95e1d3`)
  - Sound: Yellow (`#ffd93d`)

## Responsive Design

The dashboard is fully responsive:
- Desktop: Full sidebar + main content
- Tablet: Collapsible sidebar
- Mobile: Stacked layout with bottom navigation

## User Flow

1. **Landing**: Dashboard loads with first available hive selected
2. **Selection**: User clicks different hive in sidebar
3. **Data Load**: Historical telemetry fetched and displayed
4. **Live Updates**: WebSocket connects and streams real-time data
5. **Visualization**: Charts update automatically as new data arrives

## Technical Implementation

- **Framework**: React 18.2.0
- **Charts**: Recharts 2.10.3
- **HTTP Client**: Axios 1.6.5
- **WebSocket**: Native WebSocket API
- **Styling**: CSS with gradients and animations
- **Build Tool**: Create React App

## API Integration

### REST Endpoints Used:
- `GET /hives` - Fetch hive list
- `GET /hives/{device_id}/telemetry?limit=50` - Fetch historical data

### WebSocket:
- `WS /ws/hive/{device_id}/telemetry` - Live telemetry stream

## Screenshot Descriptions

### 1. Dashboard with Live Data
Shows the main dashboard with:
- Header with "Live" status indicator
- Hive sidebar with multiple hives
- Current metrics cards showing real-time values
- Time-series charts with updating data

### 2. Metric Cards Detail
Close-up of the four metric cards:
- Temperature card with thermometer icon
- Humidity card with water drop icon
- Weight card with scale icon
- Sound card with speaker icon

### 3. Chart Interaction
Charts showing:
- Temperature and humidity trends over time
- Weight stability
- Sound level variations
- Time axis with 5-minute intervals

### 4. Multi-Hive View
Sidebar showing:
- Multiple registered hives
- Active hive highlighted
- Hive names and locations
- Bee icons for visual identification

## Accessibility

- Semantic HTML structure
- ARIA labels for interactive elements
- Keyboard navigation support
- High contrast ratios for text
- Icon + text labels for clarity

## Performance

- Optimized re-renders with React hooks
- Efficient data structures for chart data
- WebSocket reconnection on disconnect
- Lazy loading for chart components
- Maximum 50 data points displayed per chart

---

*Note: This is a text representation of the UI. The actual implementation uses React components with modern CSS styling for a polished, professional appearance.*
