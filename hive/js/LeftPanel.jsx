import React, { useState } from 'react';

export default function LeftPanel({isLoading, onSearch}) {
  const [inputText, setInputText] = useState('');

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  return (
    <div className="panel">
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
      {
      isLoading ? (
        <div className="loading-spinner"></div>
      ) : (
        null // or any other JSX you want to render when not loading
      )
    }
    </div>
  );
}

// export default LeftPanel;