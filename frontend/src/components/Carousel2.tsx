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

interface CarouselProps {
    carouselprop: string;
  }

  const Carousel: React.FC<CarouselProps> = ({ carouselprop }) => {
  var genre = ""
  genre = carouselprop;
  const [cards, setCards] = useState<React.ReactElement[]>([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [books, setBooks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [slideDirection, setSlideDirection] = useState<
    "right" | "left" | undefined
  >("left");
  const cardsPerPage = 1;
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
    axios.get(`http://127.0.0.1:5000/books/search_genre/${carouselprop}`)
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
    console.log(carouselprop)
  return (
    <div>
    <Typography>{carouselprop}</Typography>
    <Box
      sx={{
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        alignContent: "center",
        justifyContent: "center",
        height: "100%",
        width: "100%",
        marginTop: "40px",
      }}
    >
    <IconButton
        onClick={handlePrevPage}
        sx={{ margin: 5, color:"white" }}
        disabled={currentPage === 0}
      >
        {/* this is the button that will go to the previous page you can change these icons to whatever you wish*/}
        <NavigateBeforeIcon />
    </IconButton>
    <Box sx={{ width: `100%`, height: "100%" }}>    
    {loading ? (<p>loading...</p>) : (
    books[0].map((book, index) => (
        <Box
            key={`book-${index}`}
            sx={{
              width: "100%",
              height: "100%",
              display: currentPage === index ? "block" : "none",
            }}
          >
            <Bookcard key={index} book={book} />
            {/* this is the slide animation that will be used to slide the cards in and out*/}
            <Slide direction={slideDirection} in={currentPage === index}>
              <Stack
                spacing={2}
                direction="row"
                alignContent="center"
                justifyContent="center"
                sx={{ width: "100%", height: "100%" }}
              >
                {/*<Bookcard book={book}/>*/}
                {/* this slices the cards array to only display the amount you have previously determined per page*/}
                {cards.slice(
                  index * cardsPerPage,
                  index * cardsPerPage + cardsPerPage
                )}
              </Stack>
            </Slide>
          </Box>
        
      ))
    )}
    </Box>
    <IconButton
        onClick={handleNextPage}
        sx={{
          margin: 5,
          color: "white"
        }}
        disabled={
          currentPage >= Math.ceil((cards.length || 0) / cardsPerPage) - 1
        }
      >
        <NavigateNextIcon />
    </IconButton>
    </Box>
    </div>
  );
}

export default Carousel;