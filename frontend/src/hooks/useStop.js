import { useEffect, useState } from "react";


export default function useStop(dataFunc){

    const [stops, setStops] = useState([]);
    const [ activeStop, setActiveStop ] = useState({activeStopName: "North Station", activeStopId: "place-north"})
    
    useEffect(() => {
      
      async function getData(){
        try{
          const stopRes = await fetch(`${process.env.REACT_APP_BASE_URL}/departures/stop/`)
          const stopJson = await stopRes.json()
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