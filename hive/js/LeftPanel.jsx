import React, { useState } from 'react';

export default function LeftPanel({isLoading, onSearch}) {
  const [inputText, setInputText] = useState('');

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  return (
    <div className="panel">
      <h1 className="left_header" >Welcome to Hive</h1>
      {/* <img src = "../static/img/android-chrome-512x512.png"/> */}
      <h1 className="left_name">Hive</h1>
      <div className = "search_container">
       <input 
        type="text"
        className="text-input" // Example class for input
        placeholder="Find me something to do..."
        value={inputText}
        onChange={handleInputChange}
      />
      <button className="search-button" onClick={onSearch}>
        Search
      </button>
      </div>
      {
      isLoading ? (
        <div className="loading-spinner">
        </div>
      ) : (
        null // or any other JSX you want to render when not loading
      )
    }
    </div>
  );
}

// export default LeftPanel;