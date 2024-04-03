import  Card  from "@mui/material/Card";
import Typography  from "@mui/material/Typography";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Button from "@mui/material/Button";



function Bookcard(book) {
  console.log(book)
  

    return ( 
        <Card sx={{ minWidth: 275 }}>
      <CardContent>
        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
          {book.book.genre}
        </Typography>
        <Typography variant="h5" component="div">
          {book.book.title}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          {book.book.author}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small">Add</Button>
      </CardActions>
    </Card>
     );
}

export default Bookcard;