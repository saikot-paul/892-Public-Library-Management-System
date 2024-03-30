from fastapi import APIRouter
from .firestore_db import db

router = APIRouter()


def get_books_by_isbn(isbn: str):
    query_ref = db.collection('all_books').where(
        'ISBN', '==', isbn, )

    docs = query_ref.stream()

    data = [res._data for res in docs]

    return data


@router.get("/books/search_isbn/{isbn}")
async def search_books_isbn(isbn: str):
    results = get_books_by_isbn(isbn)

    return {
        "results": results
    }


@router.get("/books/search_title/{title}")
async def get_books_by_title(title: str):

    title_arr = title.split("+")
    title_arr = [item.capitalize() for item in title_arr]
    query_ref = db.collection('all_books').where(
        'Keywords', 'array_contains_any', title_arr)

    docs = query_ref.stream()

    data = []
    for res in docs:
        data.append(res._data)

    return {
        "results": data
    }


@router.get("/books/search_genre/{genre}")
async def get_books_by_genre(genre: str):

    gen = genre.capitalize()
    query_ref = db.collection('all_books').where(
        'Genre', '==', genre)

    docs = query_ref.stream()

    data = []
    for res in docs:
        data.append(res._data)

    return {
        "results": data
    }
