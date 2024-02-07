import { useEffect, useState } from "react";
import StopSelector from "./components/LocationSelector"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

import useStop from "./hooks/useStop";

function App() {

  const [ loading, setLoading ] = useState(false)
  const [ departures, setDepartures ] = useState({eastern_date: undefined, eastern_time: undefined, departures: []})
  const { handleChange, stops, activeStop} = useStop(getData)

  async function getData(mbtaId){
      try{
        setLoading(true)
        const departureData = await fetch(`${process.env.REACT_APP_BASE_URL}/departures/stop/${mbtaId}`)
        const departureJson = await departureData.json()
        setDepartures(departureJson)
        setLoading(false)
      } catch(e){
        console.log(e)
      }
    }

  useEffect(() => {
    getData(activeStop.activeStopId)
    return () => {
      setDepartures({eastern_date: undefined, eastern_time: undefined, departures: []})
    }
  }, [])
  
  function convertDate(date){
    return new Date(date).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });

  }

  console.log(departures.departures)
  
  return (
    <div className="container">
      <div styles={{display: "flex"}}>
      <h1>Departures</h1>
      <h1>Current Stop: {activeStop.activeStopName}</h1>
      </div>
        <div className="time-container">
            <h4>Current Date: { departures.eastern_date }</h4>
            <h4>Current Time: { departures.eastern_time }</h4>
        </div>
        <StopSelector handleChange={handleChange} stops={stops} activeStop={activeStop}/>
        <table aria-label="Departure board">
            <thead>
                <tr>
                    <th>Carrier</th>
                    <th>Arrival Time</th>
                    <th>Departure Time</th>
                    <th>Destination</th>
                    <th>Train</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr >
                  <td colSpan="5" style={{ textAlign: 'center', verticalAlign: 'middle', fontSize: '20px', padding: '20px', display: 'flex'}}>
                    <FontAwesomeIcon icon={faSpinner} spin /> Loading...
                  </td>
                </tr>
              ) : (
                departures.departures.length > 0 &&
                departures.departures.map(departure => (
                  <tr style={{color: departure.has_prediction ? "#6495ED": null} }>
                      <td>{departure.carrier}</td>
                      <td>{departure.arrival_time ? convertDate(departure.arrival_time) : null}</td>
                      <td>{departure.departure_time ? convertDate(departure.departure_time) : null}</td>
                      <td>{departure.destination}</td>
                      <td>{departure.vehicle_id}</td>
                      <td>{departure.status}</td>
                  </tr>
                ))
              )}
              {!loading && departures.departures.length === 0 ? (
                <tr>
                  <td>No upcoming commuter rail stops.</td>
                </tr>
              ) : null}
            </tbody>
        </table>
    </div>
  );
}

export default App;
