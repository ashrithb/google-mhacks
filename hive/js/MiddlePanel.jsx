import React from 'react';

function MiddlePanel({ results }) {
  return (
    <div className="panel">
      {results.map((result, index) => (
        <div key={index} className="result-box">
          {/* Display result content here */}
          {result}
        </div>
      ))}
    </div>
  );
}

export default MiddlePanel;