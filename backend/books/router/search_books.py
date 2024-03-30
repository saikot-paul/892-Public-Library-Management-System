from fastapi import APIRouter
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

router = APIRouter()

creds = credentials.Certificate('./config.json')
firebase_admin.initialize_app(creds)
db = firestore.client()


@router.get("/books/search_isbn/{isbn}")
async def get_books(isbn: str):
    query_ref = db.collection('all_books').where(
        'ISBN', '==', isbn)

    docs = query_ref.stream()

    data = []
    for res in docs:
        data.append(res._data)

    return {
        "results": data
    }


@router.get("/books/search_title/{title}")
async def get_books(title: str):
    query_ref = db.collection('all_books').where(
        'Title', '==', title)

    docs = query_ref.stream()

    data = []
    for res in docs:
        data.append(res._data)

    return {
        "results": data
    }
