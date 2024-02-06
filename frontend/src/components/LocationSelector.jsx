import React from 'react';


function StopSelector({ handleChange, stops, activeStop}) {

  return (
    <div>
      <select onChange={handleChange} defaultValue={activeStop.activeStopName}>
        <option value={activeStop.activeStopName} disabled>{activeStop.activeStopName}</option>
        {stops.map(stop => (
          <option key={stop.mbta_id} value={stop.mbta_id} data-name={stop.name}>{stop.name}</option>
        ))}
      </select>
    </div>
  );
}

export default StopSelector;
