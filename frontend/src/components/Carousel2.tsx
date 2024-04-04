import axios from 'axios';
import React, { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import { IconButton, Typography } from "@mui/material";
import NavigateBeforeIcon from "@mui/icons-material/NavigateBefore";
import NavigateNextIcon from "@mui/icons-material/NavigateNext";
import Slide from "@mui/material/Slide";
import Stack from "@mui/material/Stack";
import Bookcard from "./Bookcard";
import Card from '@mui/material/Card';

interface Book {
  title: string;
  author: string;
  genre: string;
  isbn: string;
  copies: number; // Add copies field to Book interface
  bookId: number;
  status: boolean;
}

function Carousel() {
  const [cards, setCards] = useState<React.ReactElement[]>([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [books, setBooks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [slideDirection, setSlideDirection] = useState<
    "right" | "left" | undefined
  >("left");
  const cardsPerPage = 3;
  const containerWidth = cardsPerPage * 33; // rem per card
  // this is just a dummy array of cards it uses the MUI card demo and repeats it 10 times
  const duplicateCards: React.ReactElement[] = Array.from(
    { length: 20 },
    (_, i) => <Card key={i} />
  );

  // these two functions handle changing the pages
  const handleNextPage = () => {
    setSlideDirection("left");
    setCurrentPage((prevPage) => prevPage + 1);
  };

  const handlePrevPage = () => {
    setSlideDirection("right");
    setCurrentPage((prevPage) => prevPage - 1);
  };

  // This useEffect is really just for demonstration purposes
  // it sets the cards to the duplicateCards array
  // you can remove this and replace it with your own useEffect
  // or if your page is static you can just set the cards to the array
  // at the top of the file
  /*
  useEffect(() => {
    setCards(duplicateCards);
    // eslint-disable-next-line
  }, []);*/
  // this sets the container width to the number of cards per page * 250px
  // which we know because it is defined in the card component
  


    

    useEffect(() => {
        fetchData(); // Fetch data when component mounts
        console.log("loading: "+loading)
        //!loading ? (console.log(books)) : null
      }, []);

    async function fetchData() {
        // Make API request and fetch JSON data
    axios.get('http://127.0.0.1:5000/books/search_genre/reference')
    .then(response => {
      // Parse JSON data from response
      const jsonData = response.data.data.books;
      console.log(jsonData)
      // Set the data in state
      //setBooks([...books,jsonData]);
      setBooks([jsonData]);
      setCards(duplicateCards);
      setLoading(false); // Set loading to false after data is fetched
      //console.log(books[0][1])
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
    }

    console.log(books)
    //onsole.log(books)) : null
    //I want to map books onto Bookcard book={books[i]}
    
    /*!loading ? (setCards(
        books
    )) : null;*/
    console.log(books)
    console.log(cards)
  return (
    <div>
    <Typography>Carousel</Typography>    
    {loading ? (<p>loading...</p>) : (
    //  outer box that holds the carousel and the buttons
    
    books[0].map((book, index) => (
        
        <Bookcard key={index} book={book} />
      ))
    )}
    </div>
  );
}

export default Carousel;