import axios from 'axios';
import { useEffect,useState } from 'react';
import  Card  from "@mui/material/Card";
import Typography  from "@mui/material/Typography";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Button from "@mui/material/Button";

function Bookcard() {
  const [bookdata, setData] = useState(null);

  useEffect(() => {
    // Make API request and fetch JSON data
    axios.get('http://127.0.0.1:5000/books/search_isbn/978-0-452-28423-4')
      .then(response => {
        // Parse JSON data from response
        const jsonData = response.data.data.book;
        console.log(jsonData)
        // Set the data in state
        setData(jsonData);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []); // Run once on component mount

    return ( 
        <Card sx={{ minWidth: 275 }}>
      <CardContent>
        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
          {bookdata?.genre}
        </Typography>
        <Typography variant="h5" component="div">
          {bookdata?.title}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          {bookdata?.author}
        </Typography>
        <Typography variant="body2">
          Description of the book can go here
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small">Add</Button>
      </CardActions>
    </Card>
     );
}

export default Bookcard;