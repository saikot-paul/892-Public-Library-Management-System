from fastapi import APIRouter, HTTPException
from firestore_db import db

from .borrowed_books import get_borrowed_books
from .waitlist import get_waitlist

router = APIRouter()

@router.get("/{uid}/recommendations")
def get_recommendations(uid: str):
    borrowed_books = get_borrowed_books(uid)
    waitlist_books = get_waitlist(uid)

    if len(borrowed_books + waitlist_books) == 0:
        return {"message": "No books borrowed or waitlisted. Cannot find recommendations"}

    # Downcase keys
    borrowed_books = [{key.lower(): value for key, value in book.items()} for book in borrowed_books]
    waitlist_books = [{key.lower(): value for key, value in book.items()} for book in waitlist_books]

    # Get genre with most books in waitlist + borrowed_books
    used_books = []
    genre_count = {}

    for book in (borrowed_books + waitlist_books):
        if book['isbn'] in used_books:
            continue

        # Add this book's genre to genre_count
        if book['genre'] in genre_count:
            genre_count[book['genre']] += 1
        else:
            genre_count[book['genre']] = 1

        used_books.append(book['isbn'])
    
    # Sort genre_count dictionary by values in descending order
    sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)

    # Extract the keys (genres) from the sorted genre_count
    most_popular_genres = [genre[0] for genre in sorted_genres]

    # Get books that belong to the most popular genres
    query_ref = db.collection('filtered_books').where('Genre', 'in', most_popular_genres).limit(10)

    recommended_books = [doc.to_dict() for doc in query_ref.get()]

    # Filter out books in waitlist and borrowed books
    recommended_books = [book for book in recommended_books 
                         if book['isbn'] not in [b['isbn'] for b in borrowed_books + waitlist_books]]

    recommended_books = [{key.lower(): value for key, value in book.items()} for book in recommended_books]

    return recommended_books