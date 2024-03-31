from fastapi import FastAPI

from books.router import search_books, checkout_books, crud_books
from users.router import recommendations, waitlist, loaned_books

app = FastAPI()

app.include_router(search_books.router)
app.include_router(crud_books.router)
app.include_router(checkout_books.router)

app.include_router(recommendations.router)
app.include_router(waitlist.router)
app.include_router(loaned_books.router)
