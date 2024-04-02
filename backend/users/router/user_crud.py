from fastapi import APIRouter, HTTPException
from firestore_db import db
from pydantic import BaseModel

from .borrowed_books import get_borrowed_books
from .waitlist import get_waitlist

router = APIRouter()

class UserInfo(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    contact_number: str | None = None
    postal_code: str | None = None

@router.get("/user/{uid}")
def get_user_info(uid: str):
    user_doc_ref = db.document(f'users/{uid}')

    user_doc = user_doc_ref.get()

    if user_doc.exists:
        user_doc_data = user_doc.to_dict()
        user_doc_data = {key:val for key,val in user_doc_data.items() if key not in ('borrowed_books', 'waitlist')}

        # Get borrowed books
        user_doc_data['borrowed_books'] = get_borrowed_books(uid)

        # Get waitlist books
        user_doc_data['waitlist_books'] = get_waitlist(uid)

        return user_doc_data
    else:
        raise HTTPException(404, "User not found")
    
@router.put("/user/{uid}")
def update_user_info(uid: str, u_info: UserInfo):
    user_doc_ref = db.document(f'users/{uid}')

    u_info_data = u_info.model_jump_json()

    filtered_u_info_data = {key:val for key,val in u_info_data.items() if val is not None}
    
    user_doc_ref.update(filtered_u_info_data)

    return {"message": "User {uid} information updated"}