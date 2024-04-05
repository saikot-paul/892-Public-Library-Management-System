import Typography from "@mui/material/Typography";
import Carousel1 from "../components/Carousel1";
import Carousel2 from "../components/Carousel2";
import MyCarousel from "../components/MyCarousel";
import Navbar from "../components/Navbar";
import Navbar2 from "../components/Navbar2";
import "../assets/page.css";

function Explore() {

    

    return (
        <div className="page">
        <Navbar/>
        <Typography variant="h3" sx={{mt:5}}>Explore</Typography>
        <MyCarousel carouselprop="Fiction"/>
        <MyCarousel carouselprop="Non-Fiction"/>
        <MyCarousel carouselprop="Science%20Fiction"/>
        <MyCarousel carouselprop="Reference"/>
        <MyCarousel carouselprop="Drama"/>
        <MyCarousel carouselprop="Tragedy"/>
        <MyCarousel carouselprop="Classics"/>
        </div> 
     );
}

export default Explore;