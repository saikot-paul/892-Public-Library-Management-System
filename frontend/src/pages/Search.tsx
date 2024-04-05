import axios from 'axios';
import { useParams, useLocation } from "react-router-dom";
import { useEffect,useState } from 'react';
import Typography  from "@mui/material/Typography";
import Navbar from "../components/Navbar";
import MyCarouselTitle from '../components/MyCarouselTitle';

// Custom hook to fetch searchQuery from URL
function useSearchQuery() {
    const { searchQuery } = useParams<{ searchQuery: string }>();
    return searchQuery;
  }

function Search() {
    const searchQuery = useSearchQuery();
    const location = useLocation();


    

  useEffect(() => {
    // This code will run every time the component refreshes
    console.log("Search query:", searchQuery);
  }, [searchQuery]); // Run the effect whenever searchQuery changes

    /*const { searchQuery } = useParams<{ searchQuery: string }>();
    console.log(searchQuery)

    useEffect(() => {
        // This code will run every time the component refreshes
        console.log("Search query:", searchQuery);
      }, [searchQuery]);*/

    return ( 
        <div className='page'>
            <Navbar/>
            <Typography>This is Search Page</Typography>
            <Typography>Viewing results for: "{searchQuery}"</Typography>
            <MyCarouselTitle carouselprop={searchQuery}/>
        </div>
     );
}

export default Search;