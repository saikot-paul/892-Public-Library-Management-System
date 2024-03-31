from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
from .firestore_db import db
from firebase_admin import firestore

router = APIRouter()


class DummyBook(BaseModel):
    Title: str
    Author: str
    Genre: str
    ISBN: str


class Book(DummyBook):
    Book_ID: int
    Status: bool


class id(BaseModel):
    Book_ID: int


@router.post('/books/create_book')
async def create_book(data: DummyBook):
    copy = data.model_dump()
    copy['Status'] = False

    count = db.collection('all_books').get()
    count = len(count)

    copy["Book_ID"] = count
    copy["Keywords"] = copy['Title'].split(" ")

    doc_ref = db.collection('all_books').document()
    doc_ref.set(copy)

    isbn = copy['ISBN']
    filtered_book_data = {
        'Title': copy['Title'],
        'Genre': copy['Genre'],
        'Author': copy['Author'],
        'Keywords': copy['Keywords'],
        'num_copies': 1,
        'available_copies': 1
    }

    doc_ref = db.collection('filtered_books').document(isbn)
    doc = doc_ref.get()

    if doc.exists:
        doc_ref.update({
            'num_copies': firestore.Increment(1),
            'available_copies': firestore.Increment(1)
        })
    else:
        db.collection('filtered_books').document(isbn).set(filtered_book_data)


@router.put('/books/update_book')
async def update_book(data: Book):
    doc = get_book_by_id(data)
    db.collection('all_books').document(doc.id).update(data.model_dump())


@router.delete('/books/delete_book')
async def delete_book(id: id):
    doc = get_book_by_id(id)
    if doc.exists:
        data = doc._data
        db.collection('all_books').document(doc.id).delete()

        doc_ref = db.collection('filtered_books').document(data['ISBN'])
        doc_ref.update({
            'available_copies': firestore.Increment(-1)
        })


def get_book_by_id(id: id):
    book_id = id.Book_ID

    query_ref = db.collection('all_books').where(
        'Book_ID', '==', book_id
    )

    doc = list(query_ref.stream())[0]
    return doc
