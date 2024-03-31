from db.firestore_db import db

def get_user_info(uid: str):
    user_doc_ref = db.document(f'users/{uid}')

    user_doc = user_doc_ref.get()

    if user_doc.exists:
        return user_doc.to_dict()
    else:
        return None
    