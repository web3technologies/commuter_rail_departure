import React from 'react';


function StopSelector({ handleChange, stops, activeStop}) {

  return (
    <div style={{ margin: "10px 0" }}>
      <select
        onChange={handleChange}
        defaultValue={activeStop.activeStopName}
        style={{
          width: "100%",
          padding: "8px 10px", 
          margin: "5px 0",
          backgroundColor: "#f8f8f8",
          border: "1px solid #ccc",
          borderRadius: "4px", 
          fontSize: "16px",
          cursor: "pointer",
          boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
        }}
      >
        <option value={activeStop.activeStopName} disabled>{activeStop.activeStopName}</option>
        {stops.map(stop => (
          <option key={stop.mbta_id} value={stop.mbta_id} data-name={stop.name}>{stop.name}</option>
        ))}
      </select>
    </div>

  );
}

export default StopSelector;
