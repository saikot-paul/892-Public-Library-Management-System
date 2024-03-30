import firebase_admin
from random import randint
from firebase_admin import credentials
from firebase_admin import firestore

creds = credentials.Certificate('./config.json')
firebase_admin.initialize_app(creds)

db = firestore.client()

books_data = [
    {"Title": "To Kill a Mockingbird", "Author": "Harper Lee",
        "Genre": "Fiction", "ISBN": "978-0-06-112008-4"},
    {"Title": "The Kite Runner", "Author": "Khaled Hosseini",
        "Genre": "Fiction", "ISBN": "978-0-374-52907-2"},
    {"Title": "Moby Dick", "Author": "Herman Melville",
        "Genre": "Fiction", "ISBN": "978-0-14-243724-7"},
    {"Title": "1984", "Author": "George Orwell",
        "Genre": "Science Fiction", "ISBN": "978-0-452-28423-4"},
    {"Title": "The Great Gatsby", "Author": "F. Scott Fitzgerald",
        "Genre": "Fiction", "ISBN": "978-0-7432-7356-5"},
    {"Title": "Guinness World Records", "Author": "Guinness World Records",
        "Genre": "Non-Fiction", "ISBN": "978-1-910561-64-5"},
    {"Title": "Oxford Dictionary", "Author": "Oxford University Press",
        "Genre": "Reference", "ISBN": "978-0-19-957112-3"},
]

result = []
cur = 0
for item in (books_data):
    copies = randint(1, 3)
    for i in range(copies):
        temp = item.copy()
        temp['Status'] = False
        temp['Book_ID'] = cur
        temp['Keywords'] = temp['Title'].split("")
        cur += 1

        doc_ref = db.collection('all_books').document()
        doc_ref.set(temp)
