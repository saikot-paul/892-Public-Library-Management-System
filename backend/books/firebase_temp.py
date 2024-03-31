import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
creds = credentials.Certificate('./router/config.json')
firebase_admin.initialize_app(creds)

# Firestore client
db = firestore.client()

# Fetch documents from Firestore
docs = db.collection('all_books').get()
filtered = {}

# Process documents
for doc in docs:
    data = doc.to_dict()  # Use to_dict() to get document data
    isbn = data['ISBN']

    # Initialize or update the entry for this ISBN
    if isbn not in filtered:
        filtered[isbn] = {
            'Title': data['Title'],
            'Genre': data['Genre'],
            'Author': data['Author'],
            'Keywords': data['Title'].split(" "),
            'num_copies': 1,
            'available_copies': 0 if data['Status'] else 1,
            'checkout_list': []
        }
    else:
        filtered[isbn]['num_copies'] += 1
        if not data['Status']:  # Increment available_copies if not checked out
            filtered[isbn]['available_copies'] += 1

# Print the summarized data
for key, item in filtered.items():
    db.collection('filtered_books').document(key).set(item)
