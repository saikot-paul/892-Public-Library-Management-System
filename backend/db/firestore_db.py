import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

creds = credentials.Certificate('db/config.json')
firebase_admin.initialize_app(creds)
db = firestore.client()
