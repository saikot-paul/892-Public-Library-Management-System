from fastapi import APIRouter, HTTPException
from firestore_db import db

router = APIRouter()

# TODO: handle this endpoint such that only a user can retrieve the waitlist
#       that belongs to their account
@router.get("/{uid}/waitlist")
def get_waitlist(uid: str):
    # Get waitlist
    user_doc_ref = db.document(f'users/{uid}')
    user_doc = user_doc_ref.get()
    user_data = user_doc.to_dict()
    waitlist = user_data.get('waitlist', [])

    if waitlist is None:
        return []

    # Get book info
    waitlist_books = []
    for book_ref in waitlist:
        book_doc = book_ref.get()

        # TODO: error handling if book_doc does not exist
        if book_doc.exists:
            waitlist_books.append(book_doc.to_dict())
        else:
            print(f"Book {book_doc.id} does not exist")

    waitlist_books = [{key.lower(): value for key, value in book.items()} for book in waitlist_books]
    return waitlist_books

@router.post("/{uid}/waitlist/{isbn}")
def append_to_waitlist(uid: str, isbn: str):
    # Get waitlist
    user_doc_ref = db.document(f'users/{uid}')
    user_doc = user_doc_ref.get()
    user_data = user_doc.to_dict()
    waitlist = user_data.get('waitlist', [])

    # Check if book exists
    book_doc_ref = db.document(f'filtered_books/{isbn}')
    book_doc = book_doc_ref.get()

    if not book_doc.exists:
        raise HTTPException(404, f"Book {isbn} not found")
    
    # Check if book already exists in waitlist
    if book_doc_ref in waitlist:
        raise HTTPException(409, f"Book {isbn} already on user {uid}'s waitlist")

    # Append book doc ref to waitlist
    waitlist.append(book_doc_ref)

    # Update user doc with new wishlist
    user_doc_ref.update({'waitlist': waitlist})

    return {"message": f"Book {isbn} appended to waitlist successfully."}

@router.delete("/{uid}/waitlist/{isbn}")
def delete_from_waitlist(uid: str, isbn: str):
    # Get waitlist
    user_doc_ref = db.document(f'users/{uid}')
    user_doc = user_doc_ref.get()
    user_data = user_doc.to_dict()
    waitlist = user_data.get('waitlist', [])

    # Construct reference to filtered book doc
    filtered_book_doc_ref = db.document(f'filtered_books/{isbn}')

    if filtered_book_doc_ref not in waitlist:
        raise HTTPException(404, f"Book {isbn} not in waitlist")
    
    # Delete book from user waitlist
    waitlist.remove(filtered_book_doc_ref)
    user_doc_ref.update({'waitlist': waitlist})
    
    return {"message": f"Book {isbn} successfully removed."}