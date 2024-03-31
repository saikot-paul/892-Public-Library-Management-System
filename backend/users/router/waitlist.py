from fastapi import APIRouter, HTTPException
from firestore_db import db

router = APIRouter()



# TODO: handle this endpoint such that only a user can retrieve the waitlist
#       that belongs to their account
@router.get("/{user}/waitlist")
def get_waitlist(user: str):
    doc_ref = db.document('users/{user}/wishlist')

    doc = doc_ref.get()

    if doc.exists:
        wishlist = doc.to_dict()
    else:
        raise HTTPException(404, "User's wishlist not found")

    print(wishlist)

    return