from fastapi import APIRouter
from db.firestore_db import db

router = APIRouter()


def get_books_by_isbn(isbn: str):
    query_ref = db.collection('filtered_books').where(
        'ISBN', '==', isbn, )

    docs = query_ref.stream()

    data = [res._data for res in docs]

    return data


@router.get("/books/search_isbn/{isbn}")
async def search_books_isbn(isbn: str):
    doc_ref = db.collection('filtered_books').document(isbn)

    doc = doc_ref.get()

    if doc.exists:
        return {
            "results": {
                "empty": False,
                "data": doc_ref.get().to_dict()
            }
        }
    else:
        return {
            "results": {
                "empty": True
            }
        }


@router.get("/books/search_title/{title}")
async def get_books_by_title(title: str):

    title_arr = title.split("+")
    title_arr = [item.capitalize() for item in title_arr]
    query_ref = db.collection('filtered_books').where(
        'Keywords', 'array_contains_any', title_arr)

    docs = query_ref.stream()

    data = []
    for res in docs:
        data.append(res._data)

    if (len(data) == 0):
        return {
            "results": {
                "empty": True,
                "data": data
            }
        }
    else:
        return {
            "results": {
                "empty": False,
                "data": data
            }
        }


@router.get("/books/search_genre/{genre}")
async def get_books_by_genre(genre: str):

    gen = genre.capitalize()
    query_ref = db.collection('filtered_books').where(
        'Genre', '==', gen)

    docs = query_ref.stream()

    data = []
    for res in docs:
        data.append(res._data)

    if (len(data) == 0):
        return {
            "results": {
                "empty": True,
                "data": data
            }
        }
    else:
        return {
            "results": {
                "empty": False,
                "data": data
            }
        }
