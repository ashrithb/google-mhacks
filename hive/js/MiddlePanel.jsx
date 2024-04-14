import React from 'react';

function MiddlePanel({ results }) {
  results =[
    {
      event_description:" Test Event 1",
      friends:"Bob, Evans",
      time: "Friday, 5:30 PM"
    },
    {
      event_description: " Test Event 2",
      friends: "Bob",
      time: "Sunday, 10:30 PM"
    }
  ]
  return (
    <div className="panel">
      <h1 className="left_header" >Recommended Events</h1>
      {results.map((result, index) => (
        <div key={index} className="result-box">
          {/* <div className="event-title">{result.event_description}</div>
          <div className="event-time">{result.time}</div>
          <div className="event-friends"> */}
          <Event result={result}/>
            {/* Friends involved: {result.friends.join(', ')} */}
          </div>
      ))}
    </div>
  );
}


function Event({result})
{
  return (
    <div className="event-container">
      
          <div className = "event-title-friends-container">
          <div className="event-title">{result.event_description}</div>
          <div className="event-friends"> {result.friends}</div>
          </div>
          <div className="event-time">{result.time}</div>
          
        
      
    </div>
  );
}

export default MiddlePanel;