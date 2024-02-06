import { useEffect, useState } from "react";


export default function useStop(dataFunc){

    const [stops, setStops] = useState([]);
    const [ activeStop, setActiveStop ] = useState({activeStopName: "North Station", activeStopId: "place-north"})
    
    useEffect(() => {
      
      async function getData(){
        try{
          const stopRes = await fetch("http://localhost:8000/departures/stop-names/")
          const stopJson = await stopRes.json()
          stopJson.unshift( {
              "name": "All Stops",
              "mbta_id": ""
          })
          setStops(stopJson)
        } catch(e){
          console.log(e)
        }
      }
      getData()
      return () => {}
    }, [])
  
    const handleChange = (event) => {
        const mbta_id = event.target.value;
        const name = event.target.options[event.target.selectedIndex].getAttribute('data-name');
        setActiveStop({activeStopName:name, activeStopId:"place-north"})
        dataFunc(mbta_id);
      };
      

    return { handleChange, stops, activeStop}
}