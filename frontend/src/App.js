import { useEffect, useState } from "react";
import StopSelector from "./components/LocationSelector"

import useStop from "./hooks/useStop";

function App() {

  const [ loading, setLoading ] = useState(false)
  const [ departures, setDepartures ] = useState({eastern_date: undefined, eastern_time: undefined, departures: []})
  const { handleChange, stops, activeStop} = useStop(getData)

  async function getData(mbtaId){
      try{
        setLoading(true)
        const departureData = await fetch(`http://localhost:8000/departures/api/${mbtaId}`)
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
                    <th>Current Location</th>
                    <th>Arrival Time</th>
                    <th>Departure Time</th>
                    <th>Scheduled Departure</th>
                    <th>Final Destination</th>
                    <th>Train</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
              {
              loading ? <tr><td>Loading...</td></tr> :
              departures.departures.length > 0 && departures.departures.map(departureArr =>(
                <tr>
                  {
                    departureArr.map(val=>
                      <td>{val}</td>
                    )
                  }
                </tr>
              ))}
              {!loading && departures.departures.length == 0 ? <tr><td>No commuter rails</td></tr> : null}
            </tbody>
        </table>
    </div>
  );
}

export default App;
