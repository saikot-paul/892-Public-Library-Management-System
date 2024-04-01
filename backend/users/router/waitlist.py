from fastapi import APIRouter, HTTPException
from backend.users.grpc_server.firestore_db import db

import users_common_funcs as helper

router = APIRouter()

# TODO: handle this endpoint such that only a user can retrieve the waitlist
#       that belongs to their account
@router.get("/{uid}/waitlist")
def get_waitlist(uid: str):
    # Check if user exists
    user_dict = helper.get_user_info(uid)

    if user_dict is None:
        raise HTTPException(404, "User {uid} not found")

    # Get waitlist
    waitlist_books = []
    waitlist = user_dict.get('waitlist')

    if waitlist is None:
        return []

    # Get book info
    for book_ref in waitlist:
        book_doc = book_ref.get()

        print(f"path to book: {book_ref.path}")

        # TODO: error handling if book_doc does not exist
        if book_doc.exists:
            waitlist_books.append(book_doc.to_dict())
        else:
            print(f"Book {book_doc.id} does not exist")
    return waitlist_books

@router.post("/{uid}/waitlist/{book_id}")
def append_to_waitlist(uid: str, book_id: str):
    # Check if user exists
    user_doc_ref = db.document(f'users/{uid}')
    user_dict = helper.get_user_info(uid)

    if user_dict is None:
        raise HTTPException(404, "User {uid} not found")
    
    # Get waitlist
    waitlist = user_dict.get('waitlist', [])

    # Check if book exists
    book_doc_ref = db.document(f'all_books/{book_id}')
    book_doc = book_doc_ref.get()

    if not book_doc.exists:
        raise HTTPException(404, f"Book {book_id} not found")
    
    # Append book doc ref to waitlist
    waitlist.append(book_doc_ref)

    # Update user doc with new wishlist
    user_doc_ref.update({'waitlist': waitlist})

    return {"message": f"Book {book_id} appended to waitlist successfully."}

@router.delete("/{uid}/waitlist/{book_id}")
def delete_from_waitlist(uid: str, book_id: str):
    # Check if user exists
    user_doc_ref = db.document(f'users/{uid}')
    user_dict = helper.get_user_info(uid)

    if user_dict is None:
        raise HTTPException(404, "User {uid} not found")
    
    # Get waitlist
    waitlist = user_dict.get('waitlist', [])

    # Construct reference to book doc
    book_doc_ref = db.document(f'/all_books/{book_id}')

    if book_doc_ref not in waitlist:
        raise HTTPException(404, "Book {book_id} not in waitlist")
    
    # Delete book from user waitlist
    waitlist.remove(book_doc_ref)
    user_doc_ref.update({'waitlist': waitlist})
    
    return {"message": f"Book {book_id} successfully removed."}