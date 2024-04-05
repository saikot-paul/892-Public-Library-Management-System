import axios from 'axios';
import { useEffect,useState } from 'react';
import Typography  from "@mui/material/Typography";
import Bookcard from "../components/Bookcard";
import Navbar from "../components/Navbar";



function Home() {
    const [bookdata, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData(); // Fetch data when component mounts
      }, []);

    async function fetchData() {
        // Make API request and fetch JSON data
    axios.get('http://127.0.0.1:5000/books/search_isbn/978-0-452-28423-4')
    .then(response => {
      // Parse JSON data from response
      const jsonData = response.data.data.book;
      console.log(jsonData)
      // Set the data in state
      setData(jsonData);
      setLoading(false); // Set loading to false after data is fetched
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
    }

    return ( 
        <div className='page'>
            <Navbar/>
            <Typography>This is homepage</Typography>
            {loading ? (
                <p>Loading...</p>
            ) : (
                <Bookcard book={bookdata}/>
            )}
        </div>
     );
}

export default Home;