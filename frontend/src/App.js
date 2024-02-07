import { useEffect, useState } from "react";
import StopSelector from "./components/LocationSelector"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

import useStop from "./hooks/useStop";



const buttonStyle = {
  padding: "10px 20px",
  margin: "10px",
  cursor: "pointer",
  backgroundColor: "#007bff",
  color: "white",
  border: "none",
  borderRadius: "5px",
  fontSize: "16px",
  fontWeight: "bold",
  boxShadow: "0 2px 4px rgba(0,0,0,0.2)",
  transition: "background-color 0.3s",
  outline: "none",
  width: "100%", // Ensure the button fills the container
};


function App() {

  const [ loading, setLoading ] = useState(false)
  const [ refreshing, setRefreshing ] = useState(false)
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
    return new Date(date).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true,  timeZone: 'America/New_York' });

  }

  async function refreshData(){
    try{
      setRefreshing(true)
      const departureData = await fetch(`${process.env.REACT_APP_BASE_URL}/departures/stop/${activeStop.activeStopId}`)
      const departureJson = await departureData.json()
      setDepartures(departureJson)
      setRefreshing(false)
    } catch (e) {
      console.log(e)
    }
  }
  
  return (
    <div className="container">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center"}}>
        <div style={{ textAlign: "left" }}>
          <h4>{new Date(departures.eastern_date).toLocaleDateString('en-US', { weekday: 'long' })}</h4>
          <h4>{departures.eastern_date}</h4>
        </div>
        <h1>{activeStop.activeStopName} Information</h1>
        <div style={{ textAlign: "right" }}>
          <h4>Current Time:</h4>
          <h4>{departures.eastern_time}</h4>
        </div>
      </div>
      <div style={{display: "flex", justifyContent: "space-between"}}>
        <StopSelector handleChange={handleChange} stops={stops} activeStop={activeStop}/>
        <div style={{width: "10%", display: "flex", justifyContent: "center", alignItems: "center"}}>
          {
            refreshing ?
            <FontAwesomeIcon icon={faSpinner} spin />
            :
            <button style={buttonStyle} onClick={refreshData}>Refresh</button>
          }
        </div>
      </div>
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
