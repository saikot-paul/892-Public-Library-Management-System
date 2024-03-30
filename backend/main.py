from fastapi import FastAPI

from books.router import search_books, create_books, checkout_books

app = FastAPI()

app.include_router(search_books.router)
app.include_router(create_books.router)
app.include_router(checkout_books.router)
