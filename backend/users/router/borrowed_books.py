from fastapi import APIRouter, HTTPException
from firestore_db import db

router = APIRouter()

@router.get("/{uid}/borrowed_books")
def get_borrowed_books(uid: str):
    borrowed_books_ref = db.collection(f'users/{uid}/borrowed_books')
    borrowed_books = borrowed_books_ref.get()

    if len(borrowed_books) == 0:
        return {"message": f"User {uid} has no borrowed books."}

    ret_borrowed_books = []
    for book in borrowed_books:
        # Get book data
        book_data = book.to_dict()
        all_books_book_data = book_data['all_books_doc_ref'].get().to_dict()

        print(all_books_book_data)

        # Change all keys to lower case
        all_books_book_data = {key.lower():val for key,val in all_books_book_data.items()}

        ret_borrowed_books.append(all_books_book_data)
    
    return ret_borrowed_books
