from fastapi import FastAPI

from books.router import search_books, checkout_books, crud_books

app = FastAPI()

app.include_router(search_books.router)
app.include_router(crud_books.router)
app.include_router(checkout_books.router)
