import React from 'react';
import './HiveList.css';

function HiveList({ hives, selectedHive, onSelectHive }) {
  return (
    <div className="hive-list">
      {hives.length === 0 ? (
        <p className="no-hives">No hives registered</p>
      ) : (
        hives.map(hive => (
          <div
            key={hive.id}
            className={`hive-item ${selectedHive?.id === hive.id ? 'active' : ''}`}
            onClick={() => onSelectHive(hive)}
          >
            <div className="hive-icon">🐝</div>
            <div className="hive-info">
              <div className="hive-name">{hive.name || hive.device_id}</div>
              <div className="hive-location">{hive.location || 'Unknown'}</div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default HiveList;
