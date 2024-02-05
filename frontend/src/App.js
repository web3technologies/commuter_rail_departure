import { useEffect, useState } from "react";

function App() {

  const [loading, setLoading] = useState(false)
  const [ departures, setDepartures ] = useState({eastern_date: undefined, eastern_time: undefined, departures: []})


  useEffect(() => {
    
    async function getData(){
      try{
        setLoading(true)
        const departureData = await fetch("http://localhost:8000/departures/api")
        const departureJson = await departureData.json()
        setDepartures(departureJson)
        setLoading(false)
      } catch(e){
        console.log(e)
      }
    }

    getData()

    return () => {
      setDepartures({eastern_date: undefined, eastern_time: undefined, departures: []})
    }
  }, [])
  

  return (
    <div className="container">
        <h1>Departures</h1>
        <div className="time-container">
            <h4>Current Date: { departures.eastern_date }</h4>
            <h4>Current Time: { departures.eastern_time }</h4>
        </div>
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
            </tbody>
        </table>
    </div>
  );
}

export default App;
