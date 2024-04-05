import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import axios from 'axios';
import React, { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Bookcard from "./Bookcard";

import Card from '@mui/material/Card';
import { Typography } from '@mui/material';

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
  
  const MyCarouselTitle: React.FC<CarouselProps> = ({ carouselprop }) => {
    const [cards, setCards] = useState<React.ReactElement[]>([]);
    const [currentPage, setCurrentPage] = useState(0);
    const [slideDirection, setSlideDirection] = useState<
      "right" | "left" | undefined
    >("left");
    const cardsPerPage = 3;
    const duplicateCards: React.ReactElement[] = Array.from(
      { length: 10 },
      (_, i) => <Card key={i} />
    );
    const [books, setBooks] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
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
  
  
  
  
      useEffect(() => {
          fetchData(); // Fetch data when component mounts
          console.log(loading)
          //!loading ? (console.log(books)) : null
        }, []);
  
      async function fetchData() {
          // Make API request and fetch JSON data
      console.log(carouselprop);
      axios.get(`http://127.0.0.1:5000/books/search_title/${carouselprop}`)
      .then(response => {
        // Parse JSON data from response
        const jsonData = response.data.books;
        console.log(jsonData)
        // Set the data in state
        setBooks([jsonData]);
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
      /*
      !loading ? (setCards(
        books.map((book,i) => (
            <Bookcard key={i} book={book}/>
        )
      )
      )) : null;*/
  
    return (
      <div>
      {carouselprop=="Science%20Fiction"? (<Typography sx={{textAlign:"left", ml:10}}>Science Fiction</Typography>) : (<Typography sx={{textAlign:"left", ml:10}}>{carouselprop}</Typography>)}
      <Box
        sx={{
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
          alignContent: "center",
          justifyContent: "center",
          height: "100%",
          width: "100%",
          marginTop: "20px",
          marginBottom:"20px"
        }}
      >
        
        <Box sx={{ width: "100%", height: "100%",pb:5 }}>
        <Carousel
        additionalTransfrom={0}
        arrows
        autoPlaySpeed={3000}
        centerMode={false}
        className=""
        containerClass="container"
        dotListClass=""
        draggable
        focusOnSelect={false}
        infinite={false}
        itemClass=""
        keyBoardControl
        minimumTouchDrag={80}
        pauseOnHover
        renderArrowsWhenDisabled={false}
        renderButtonGroupOutside={false}
        renderDotsOutside={false}
        responsive={{
            desktop: {
            breakpoint: {
                max: 3000,
                min: 1024
            },
            items: 3,
            partialVisibilityGutter: 40
            },
            mobile: {
            breakpoint: {
                max: 464,
                min: 0
            },
            items: 1,
            partialVisibilityGutter: 30
            },
            tablet: {
            breakpoint: {
                max: 1024,
                min: 464
            },
            items: 2,
            partialVisibilityGutter: 30
            }
        }}
        rewind={false}
        rewindWithAnimation={false}
        rtl={false}
        shouldResetAutoplay
        showDots={false}
        sliderClass=""
        slidesToSlide={2}
        swipeable
        >
        {loading ? (<p>loading...</p>) : (
            books[0].map((book, index) => (
                    <Bookcard key={index} book={book} />
            )))
                }
        </Carousel>
        </Box>
        </Box>
    </div>
    );
  }
  
  export default MyCarouselTitle;

