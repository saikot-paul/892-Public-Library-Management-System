from fastapi import FastAPI

from router import search_books

app = FastAPI()

app.include_router(search_books.router)
