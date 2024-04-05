import Typography from "@mui/material/Typography";
import Carousel from "../components/Carousel";
import Carousel2 from "../components/Carousel2";
import Navbar from "../components/Navbar";
import "../assets/page.css";

function Explore() {

    

    return (
        <div className="page">
        <Navbar/>
        <Typography>This is explore page</Typography>
        <Carousel2 carouselprop="Fiction"/>
        <Carousel2 carouselprop="Non-Fiction"/>
        <Carousel2 carouselprop="Science%20Fiction"/>
        <Carousel2 carouselprop="Reference"/>
        </div> 
     );
}

export default Explore;