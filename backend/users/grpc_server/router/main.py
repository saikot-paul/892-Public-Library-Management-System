from fastapi import FastAPI

import recommendations
import waitlist
import borrowed_books

app = FastAPI()

app.include_router(recommendations.router)
app.include_router(waitlist.router)
app.include_router(borrowed_books.router)
