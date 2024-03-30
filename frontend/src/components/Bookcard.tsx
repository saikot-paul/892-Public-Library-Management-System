import  Card  from "@mui/material/Card";
import Typography  from "@mui/material/Typography";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Button from "@mui/material/Button";

function Bookcard() {
    return ( 
        <Card sx={{ minWidth: 275 }}>
      <CardContent>
        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
          Genre/type
        </Typography>
        <Typography variant="h5" component="div">
          Title
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          Author
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