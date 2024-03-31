import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

creds = credentials.Certificate('./firebase_stuff/config.json')
firebase_admin.initialize_app(creds)
db = firestore.client()
