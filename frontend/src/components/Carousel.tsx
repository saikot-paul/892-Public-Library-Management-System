import axios from 'axios';
import React, { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import { IconButton } from "@mui/material";
import NavigateBeforeIcon from "@mui/icons-material/NavigateBefore";
import NavigateNextIcon from "@mui/icons-material/NavigateNext";
import Slide from "@mui/material/Slide";
import Stack from "@mui/material/Stack";
import Bookcard from "./Bookcard";

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
  // setting the state variables
  // cards will be the cards that are displayed
  const [cards, setCards] = useState<React.ReactElement[]>([]);
  // currentPage is the current page of the cards that is currently displayed
  const [currentPage, setCurrentPage] = useState(0);
  // slideDirection is the direction that the cards will slide in
  const [slideDirection, setSlideDirection] = useState<
    "right" | "left" | undefined
  >("left");

  // cardsPerPage is the number of cards that will be displayed per page
  // you can modify for your needs
  const cardsPerPage = 3;
  // this is just a dummy array of cards it uses the MUI card demo and repeats it 10 times
  const duplicateCards: React.ReactElement[] = Array.from(
    { length: 10 },
    (_, i) => <Bookcard key={i} />
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
  const containerWidth = cardsPerPage * 33; // rem per card


    const [books, setBooks] = useState<Book[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData(); // Fetch data when component mounts
        console.log(loading)
        //!loading ? (console.log(books)) : null
      }, []);

    async function fetchData() {
        // Make API request and fetch JSON data
    axios.get('http://127.0.0.1:5000/books/search_genre/fiction')
    .then(response => {
      // Parse JSON data from response
      const jsonData = response.data.data.books;
      console.log(jsonData)
      // Set the data in state
      setBooks([...books, jsonData]);
      setLoading(false); // Set loading to false after data is fetched
      //console.log(books[0][1])
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
    }

    //console.log(loading)
    //onsole.log(books)) : null
    //I want to map books onto Bookcard book={books[i]}
    !loading ? (setCards(
      books.map((book,i) => (
          <Bookcard key={i} book={book}/>
      )
    )
    )) : null;

  return (
    loading ? (<p>loading...</p>) : (
    //  outer box that holds the carousel and the buttons
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
      <Box sx={{ width: `${containerWidth}%`, height: "100%" }}>
        {/* this is the box that holds the cards and the slide animation,
        in this implementation the card is already constructed but in later versions you will see how the
        items you wish to use will be dynamically created with the map method*/}
        {cards.map((book, index) => (
          <Box
            key={`book-${index}`}
            sx={{
              width: "100%",
              height: "100%",
              display: currentPage === index ? "block" : "none",
            }}
          >
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
        ))}
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
    )
  );
}

export default Carousel;