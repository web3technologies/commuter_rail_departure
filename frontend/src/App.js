import { useEffect, useState } from "react";

function App() {


  const [ departures, setDepartures ] = useState([])


  useEffect(() => {
    
    async function getData(){}
  
    return () => {
    }
  }, [])
  

  return (
    <div class="container">
        <h1>Departures</h1>
        <div class="time-container">
            {/* <h4>Current Date: {{ eastern_date }}</h4> */}
            {/* <h4>Current Time: {{ eastern_time }}</h4> */}
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
                <tr>
                    <td></td>
                </tr>
            </tbody>
        </table>
    </div>
  );
}

export default App;
