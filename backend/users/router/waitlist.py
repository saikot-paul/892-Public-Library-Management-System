from fastapi import APIRouter, HTTPException
from db.firestore_db import db

router = APIRouter()

# TODO: handle this endpoint such that only a user can retrieve the waitlist
#       that belongs to their account
@router.get("/{uid}/waitlist")
def get_waitlist(uid: str):
    doc_ref = db.document(f'users/{uid}')

    doc = doc_ref.get()

    if doc.exists:
        wishlist = doc.to_dict().get('wishlist', [])
    else:
        raise HTTPException(404, f"User {uid} wishlist not found")

    print(wishlist)

    wishlist_books = []

    for book_ref in wishlist:
        book_doc = book_ref.get()

        print(f"path to book: {book_ref.path}")

        # TODO: error handling if book_doc does not exist
        if book_doc.exists:
            wishlist_books.append(book_doc.to_dict())
        else:
            print(f"Book {book_doc.id} does not exist")
    return wishlist_books

@router.post("/{uid}/waitlist/{book_id}")
def append_to_waitlist(uid: str, book_id: str):
    # Check if user exists
    user_doc_ref = db.document(f'users/{uid}')

    user_doc = user_doc_ref.get()

    if not user_doc.exists:
        raise HTTPException(404, f"User {uid} wishlist not found")
    
    # Get wishlist
    wishlist = user_doc.to_dict().get('wishlist', [])

    # Check if book exists
    book_doc_ref = db.document(f'all_books/{book_id}')
    book_doc = book_doc_ref.get()

    if not book_doc.exists:
        raise HTTPException(404, f"Book {book_id} not found")
    
    # Append book doc ref to wishlist
    wishlist.append(book_doc_ref)

    # Update user doc with new wishlist
    user_doc_ref.update({'wishlist': wishlist})

    return {"message": f"Book {book_id} appended to wishlist successfully."}

