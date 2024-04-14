import React, { StrictMode, useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import InfiniteScroll from "react-infinite-scroll-component";
import LeftPanel from './LeftPanel';
import MiddlePanel from './MiddlePanel';
import RightPanel from './RightPanel';
import App from './Query'
// import '../styles/styles.css'; 
// const app = express();
// app.use(cors());
const root = createRoot(document.getElementById("reactEntry"));
// export default function App() {
//   const [results, setResults] = useState([]);
//   const [loading, setLoading] = useState(false);
//   // Function to update results based on input from LeftPanel
//   // const handleSearch = async () => {
//   //   try {
//   //       setLoading(true);
//   //     const response = await fetch(`https://your-api-endpoint.com/search?query=${inputText}`);
//   //     const data = await response.json(); // Parse JSON response
//   //     setLoading(false);
//   //     setResults(data); // Update results with parsed data
//   //   } catch (error) {
//   //     console.error('Error fetching data:', error);
//   //     // Handle errors (e.g., display an error message)
//   //   }
//   // };
//   const handleSearch = async (userQuery, geoIP) => {
//     try {
//         setLoading(true);
//         // Construct the URL with query parameters
//         const url = new URL(`http://localhost:5000/api`);
//         const params = { user_query: userQuery, geoip: geoIP };
//         url.search = new URLSearchParams(params).toString();
  
//         const response = await fetch(url);
//         const data = await response.json(); // Parse JSON response
//         setLoading(false);
//         setResults(data); // Update results with parsed data
//     } catch (error) {
//       console.error('Error fetching data:', error);
//       setLoading(false);
//       // Handle errors (e.g., display an error message)
//     }
//   };
  
//   return (
//     <div className="panel-container">

//       <LeftPanel onSearch={handleSearch} isLoading={true} />

//       <MiddlePanel results={results} />

//       <RightPanel />

//     </div>
//   );
// }

root.render(
    <StrictMode>
      <App />
    </StrictMode>,
);
