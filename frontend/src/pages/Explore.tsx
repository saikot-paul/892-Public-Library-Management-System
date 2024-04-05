import Typography from "@mui/material/Typography";
import Carousel1 from "../components/Carousel1";
import Carousel2 from "../components/Carousel2";
import Carousel3 from "../components/Carousel3";
import Navbar from "../components/Navbar";
import Navbar2 from "../components/Navbar2";
import "../assets/page.css";

function Explore() {

    

    return (
        <div className="page">
        <Navbar/>
        <Typography variant="h3" sx={{mt:5}}>Explore</Typography>
        <Carousel3 carouselprop="Fiction"/>
        <Carousel3 carouselprop="Non-Fiction"/>
        <Carousel3 carouselprop="Science%20Fiction"/>
        <Carousel3 carouselprop="Reference"/>
        <Carousel3 carouselprop="Drama"/>
        <Carousel3 carouselprop="Tragedy"/>
        <Carousel3 carouselprop="Classics"/>
        </div> 
     );
}

export default Explore;