import  Card  from "@mui/material/Card";
import Typography  from "@mui/material/Typography";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Button from "@mui/material/Button";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';



function Bookcard(book) {
  console.log(book)
  

    return ( 
        <Card sx={{ minWidth: 200, maxWidth:200, maxHeight:200, minHeight:200,ml:5, mr:5 }}>
      <CardContent>
        <Typography sx={{ fontSize: 10 }} color="text.secondary" gutterBottom>
          {book.book.genre}
        </Typography>
        <Typography variant="h6" component="div">
          {book.book.title}
        </Typography>
        <Typography sx={{ mb: 1.5,fontSize:14 }}  color="text.secondary">
          {book.book.author}
        </Typography>
      </CardContent>
      <CardActions sx={{alignItems:"bottom"}}>
        <Button size="small">
          <FavoriteBorderIcon/>
        </Button>
        <Button size="small">
          <AddShoppingCartIcon/>
        </Button>
      </CardActions>
    </Card>
     );
}

export default Bookcard;