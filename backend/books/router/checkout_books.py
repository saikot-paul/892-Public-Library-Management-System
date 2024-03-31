from fastapi import APIRouter
from pydantic import BaseModel
from db.firestore_db import db
from .search_books import get_books_by_isbn

router = APIRouter()


class Checkout(BaseModel):
    user_id: str
    isbn: str


@router.put('/books/checkout_books')
async def checkout_books(checkout: Checkout):

    isbn = checkout.isbn
    doc_ref = db.collection('filtered_books').document(isbn)
    doc = doc_ref.get()
    available_books = []

    if (doc.exists):
        data = doc.to_dict()
        if (data['available_copies'] >= 1):
            data['available_copies'] -= 1
            data['checkout_list'].append(checkout.user_id)
            doc_ref.update(data)

            books = get_books_by_isbn(checkout.isbn)

            for b in books:
                if not b['Status']:
                    available_books.append(b['Book_ID'])

                    documents = db.collection('all_books').where(
                        'Book_ID', '==', b['Book_ID']
                    ).stream()

                    for doc in documents:
                        db.collection('all_books').document(
                            doc.id).update({"Status": True})

                    break
