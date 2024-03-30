from fastapi import FastAPI

from router import search_books, create_books

app = FastAPI()

app.include_router(search_books.router)
app.include_router(create_books.router)
