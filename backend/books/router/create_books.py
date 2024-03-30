from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
from .firestore_db import db

router = APIRouter()


class DummyBook(BaseModel):
    Title: str
    Author: str
    Genre: str
    ISBN: str


class Book(DummyBook):
    Book_ID: int
    Status: bool


@router.post('/books/create_book')
async def create_book(data: DummyBook):
    data['Status'] = False

    count = db.collection('all_books').get()
    count = len(count)

    data["Book_ID"] = count
    data["Keywords"] = data['Title'].split(" ")

    doc_ref = db.collection('all_books').document()
    doc_ref.set(data)


@router.put('/books/edit_book')
async def edit_book(data: Book):
    book_id = data.Book_ID

    query_ref = db.collection('all_books').where(
        'Book_ID', '==', book_id
    )

    doc = list(query_ref.stream())[0]

    db.collection('all_books').document(doc.id).update(data.model_dump())
