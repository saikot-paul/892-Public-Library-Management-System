import user_pb2
import user_pb2_grpc
import firestore_db
from firestore_db import db
from firebase_admin import firestore
from concurrent import futures
import grpc
from google.protobuf import json_format
from fastapi import HTTPException

class UserServer(user_pb2_grpc.UsersServicer):
    def GetBorrowedBooks(self, request, context):
        uid = request.uid

        borrowed_books = get_borrowed_books(uid)

        all_books_response = user_pb2.AllBooksMessage()
        all_books_response.books.extend([])
        for book in borrowed_books:
            book_message = json_format.ParseDict(book, user_pb2.AllBooksBook())
            all_books_response.books.append(book_message)
        
        all_books_response.success = True
        all_books_response.message = 'Borrowed books retrieved.'
        return all_books_response
    
    def GetRecommendations(self, request, context):
        uid = request.uid

        try:
            borrowed_books = get_borrowed_books(uid)
            waitlist_books = get_waitlist(uid)

            if len(borrowed_books + waitlist_books) == 0:
                return {"message": "No books borrowed or waitlisted. Cannot find recommendations"}

            # Downcase keys
            borrowed_books = [{key.lower(): value for key, value in book.items()} for book in borrowed_books]
            waitlist_books = [{key.lower(): value for key, value in book.items()} for book in waitlist_books]

            # Get genre with most books in waitlist + borrowed_books
            used_books = []
            genre_count = {}

            for book in (borrowed_books + waitlist_books):
                if book['isbn'] in used_books:
                    continue

                # Add this book's genre to genre_count
                if book['genre'] in genre_count:
                    genre_count[book['genre']] += 1
                else:
                    genre_count[book['genre']] = 1

                used_books.append(book['isbn'])
            
            # Sort genre_count dictionary by values in descending order
            sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)

            # Extract the keys (genres) from the sorted genre_count
            most_popular_genres = [genre[0] for genre in sorted_genres]

            # Get books that belong to the most popular genres
            query_ref = db.collection('filtered_books').where('Genre', 'in', most_popular_genres).limit(10)

            recommended_books = [doc.to_dict() for doc in query_ref.get()]

            # Filter out books in waitlist and borrowed books
            recommended_books = [book for book in recommended_books 
                                if book['isbn'] not in [b['isbn'] for b in borrowed_books + waitlist_books]]

            recommended_books = [{key.lower(): value for key, value in book.items()} for book in recommended_books]
        except Exception as e:
            return user_pb2.FilteredBooksMessage(
                success = False,
                books = [],
                message = repr(e)
            )

        # Form response
        filtered_books_res = user_pb2.FilteredBooksMessage()
        filtered_books_res.books.extend([])

        for r in recommended_books:
            filtered_book = json_format.ParseDict(r, user_pb2.FilteredBooksBook())
            filtered_books_res.books.append(filtered_book)

        filtered_books_res.success = True
        filtered_books_res.message = "Retrieved recommendations successfully."
        return filtered_books_res

    # Note that if num_copies and available_copies are not found as fields in the waitlisted books, they are 0.
    # In proto3, explicit default values are not allowed, and the default value of an int32 is 0.
    def GetWaitlist(self, request, context):
        uid = request.uid

        try:
            waitlist_books = get_waitlist(uid)
        except Exception as e:
            return user_pb2.FilteredBooksMessage(
                success = False,
                books = [],
                message = repr(e)
            )

        # Form response
        filtered_books_res = user_pb2.FilteredBooksMessage()
        filtered_books_res.books.extend([])

        for book in waitlist_books:
            filtered_book = json_format.ParseDict(book, user_pb2.FilteredBooksBook())
            filtered_books_res.books.append(filtered_book)

        return filtered_books_res

    def AppendToWaitlist(self, request, context):
        uid = request.uid
        isbn = request.isbn

        try:
            # Get waitlist
            user_doc_ref = db.document(f'users/{uid}')
            user_doc = user_doc_ref.get()
            user_data = user_doc.to_dict()
            waitlist = user_data.get('waitlist', [])

            # Check if book exists
            book_doc_ref = db.document(f'filtered_books/{isbn}')
            book_doc = book_doc_ref.get()

            if not book_doc.exists:
                raise HTTPException(404, f"Book {isbn} not found")
            
            # Check if book already exists in waitlist
            if book_doc_ref in waitlist:
                raise HTTPException(409, f"Book {isbn} already on user {uid}'s waitlist")

            # Append book doc ref to waitlist
            waitlist.append(book_doc_ref)

            # Update user doc with new wishlist
            user_doc_ref.update({'waitlist': waitlist})

        except HTTPException as e:
            return_msg = user_pb2.SimpleMessage(
                success = False,
                error_code = e.status_code,
                message = e.detail
            )
            return return_msg
        except Exception as e:
            return_msg = user_pb2.SimpleMessage(
                success = False,
                error_code = 500,
                message = repr(e)
            )
            return return_msg

        return user_pb2.SimpleMessage(
            success = True,
            message = f"Book {isbn} appended to waitlist successfully."
        )

    def DeleteFromWaitlist(self, request, context):

        uid = request.uid
        isbn = request.isbn

        try:
            # Get waitlist
            user_doc_ref = db.document(f'users/{uid}')
            user_doc = user_doc_ref.get()
            user_data = user_doc.to_dict()
            waitlist = user_data.get('waitlist', [])

            # Construct reference to filtered book doc
            filtered_book_doc_ref = db.document(f'filtered_books/{isbn}')

            if filtered_book_doc_ref not in waitlist:
                raise HTTPException(404, f"Book {isbn} not in waitlist")
            
            # Delete book from user waitlist
            waitlist.remove(filtered_book_doc_ref)
            user_doc_ref.update({'waitlist': waitlist})

        except HTTPException as e:
            return user_pb2.SimpleMessage(
                success = False,
                error_code = e.status_code,
                message = e.detail
            )
        except Exception as e:
            return user_pb2.SimpleMessage(
                success = False,
                message = repr(e)
            )

        return user_pb2.SimpleMessage(
            success = True,
            message = f"Book {isbn} successfully removed."
        )

    def GetAllUsersInfo(self, request, context):
        print("GetAllUsersInfo()")

        # get uids of all users
        users_ref = db.collection('users')
        all_user_docs = users_ref.list_documents()
        user_ids = [doc.id for doc in all_user_docs]

        all_users_info = []

        for uid in user_ids:
            try:
                user_info_data = get_user_info(uid)
            except HTTPException as e:
                return user_pb2.UserInfoMessage(
                    success = False,
                    error_code = e.status_code,
                    message = e.detail
                )
            except Exception as e:
                return user_pb2.UserInfoMessage(
                    success = False,
                    error_code = 500,   
                    message = "Internal server error"
                )

            user_info_msg = json_format.ParseDict(user_info_data, user_pb2.UserInfo())

            if 'waitlist_books' in user_info_data:
                user_info_msg.waitlist_books.extend([])

                for book in user_info_data['waitlist_books']:
                    filtered_book = json_format.ParseDict(book, user_pb2.FilteredBooksBook())
                    user_info_msg.waitlist_books.append(filtered_book)

            if 'borrowed_books' in user_info_data:
                user_info_msg.borrowed_books.extend([])

                for book in user_info_data['borrowed_books']:
                    book_message = json_format.ParseDict(book, user_pb2.AllBooksBook())
                    user_info_msg.borrowed_books.append(book_message)

            all_users_info.append(user_info_msg)

        return user_pb2.AllUsersInfoMessage(
            success = True,
            user_info = all_users_info,
            message = f"Retrieved {uid} info successfully."
        )

    def GetUserInfo(self, request, context):
        uid = request.uid

        try:
            user_doc_data = get_user_info(uid)
                
        except HTTPException as e:
            return user_pb2.UserInfoMessage(
                success = False,
                error_code = e.status_code,
                message = e.detail
            )
        except Exception as e:
            return user_pb2.UserInfoMessage(
                success = False,
                error_code = 500,   
                message = "Internal server error"
            )

        user_info_msg = json_format.ParseDict(user_doc_data, user_pb2.UserInfo())

        if 'waitlist_books' in user_doc_data:
            user_info_msg.waitlist_books.extend([])

            for book in user_doc_data['waitlist_books']:
                filtered_book = json_format.ParseDict(book, user_pb2.FilteredBooksBook())
                user_info_msg.waitlist_books.append(filtered_book)

        if 'borrowed_books' in user_doc_data:
            user_info_msg.borrowed_books.extend([])

            for book in user_doc_data['borrowed_books']:
                book_message = json_format.ParseDict(book, user_pb2.AllBooksBook())
                user_info_msg.borrowed_books.append(book_message)

        return user_pb2.UserInfoMessage(
            success = True,
            user_info = user_info_msg,
            message = f"Retrieved {uid} info successfully."
        )

    def UpdateUserInfo(self, request, context):
        req_data = {field.name: getattr(request, field.name) for field in request.DESCRIPTOR.fields}

        # Get key value pairs to be updated
        update_data = {key:val for key,val in req_data.items() if key != 'uid' and val != ''}

        db.document(f"users/{req_data['uid']}").update(update_data)

        return user_pb2.SimpleMessage(
            success = True,
            message = f"Successfully updated {req_data.get('uid')} info"
        )

    def CreateUser(self, request, context):
        req_data = {field.name: getattr(request, field.name) for field in request.DESCRIPTOR.fields}

        user_info = {key:val for key,val in req_data.items() if val != ''}

        print(user_info)

        db.document(f"users/{req_data['uid']}").set(user_info)

        return user_pb2.SimpleMessage(
            success = True,
            message = f"Successfully created user {req_data['uid']}"
        )

    def DeleteUser(self, request, context):
        uid = request.uid

        user_doc_ref = db.document(f'users/{uid}')
        user_doc = user_doc_ref.get()

        if not user_doc.exists:
            return user_pb2.SimpleMessage(
                success = False,
                error_code = 404,
                message = f"Unable to find user {uid}"
            )

        user_doc_data = user_doc.to_dict()

        # if the user has borrowed books, return them
        sub_col_names = [sub_col.id for sub_col in user_doc_ref.collections()]
        if 'borrowed_books' in sub_col_names:
            borrowed_books_col_ref = db.collection(f'{user_doc_ref.path}/borrowed_books')
            for borrowed_book_data in borrowed_books_col_ref.get():
                return_book(uid, borrowed_book_data.get('book_id'))
                
        user_doc_ref.delete()

        return user_pb2.SimpleMessage(
            success = True,
            message = "Successfully deleted user"
        )


def get_borrowed_books(uid: str):
    borrowed_books_ref = db.collection(f'users/{uid}/borrowed_books')
    borrowed_books = borrowed_books_ref.get()

    if len(borrowed_books) == 0:
        return []

    ret_borrowed_books = []
    for book in borrowed_books:
        # Get book data
        book_data = book.to_dict()
        all_books_book_data = book_data['all_books_doc_ref'].get().to_dict()

        print(all_books_book_data)

        # Change all keys to lower case
        all_books_book_data = {key.lower():val for key,val in all_books_book_data.items()}

        ret_borrowed_books.append(all_books_book_data)
    
    return ret_borrowed_books

def return_book(uid: str, book_id: int):
    print("return_book()")

    # Use batch such that write operations are performed as one unit
    batch = db.batch()

    # Get the book doc info
    query_ref = db.collection('all_books') \
                    .where('Book_ID', '==', book_id) \
                    .where('borrowed_by', '==', uid)
    returning_books = query_ref.get()

    if len(returning_books) != 1:
        return

    ret_book_data = returning_books[0].to_dict()
    isbn = ret_book_data['ISBN']

    # Get the document referencing the borrowed book
    borrowed_book_doc_ref = db.document(f'users/{uid}/borrowed_books/{returning_books[0].id}')
    borrowed_book_doc = borrowed_book_doc_ref.get()
    borrowed_book_data = borrowed_book_doc.to_dict()

    if not borrowed_book_doc.exists:
        return

    # Increment available books counter in filtered_books
    filtered_books_doc_data = borrowed_book_data['filtered_books_doc_ref'].get().to_dict()
    filtered_books_doc_data['checkout_list'].remove(uid)
    batch.update(borrowed_book_data['filtered_books_doc_ref'], {
        'available_copies': filtered_books_doc_data['available_copies'] + 1,
        'checkout_list': filtered_books_doc_data['checkout_list']
    })

    # Change the borrowed status of the book in all_books to false
    batch.update(borrowed_book_data['all_books_doc_ref'], {
        'Status': False,
        'borrowed_by': firestore.DELETE_FIELD
    })

    # Delete borrowed book doc from user indicating book has been returned
    batch.delete(borrowed_book_doc_ref)

    batch.commit()

    return

def get_waitlist(uid: str):
    # Get waitlist
    user_doc_ref = db.document(f'users/{uid}')
    user_doc = user_doc_ref.get()
    user_data = user_doc.to_dict()
    waitlist = user_data.get('waitlist', [])

    if waitlist is None:
        return []

    # Get book info
    waitlist_books = []
    for book_ref in waitlist:
        book_doc = book_ref.get()

        # TODO: error handling if book_doc does not exist
        if book_doc.exists:
            waitlist_books.append(book_doc.to_dict())
        else:
            print(f"Book {book_doc.id} does not exist")

    waitlist_books = [{key.lower(): value for key, value in book.items()} for book in waitlist_books]
    return waitlist_books

def get_user_info(uid: str):
    user_doc_ref = db.document(f'users/{uid}')

    user_doc = user_doc_ref.get()

    if not user_doc.exists:
        raise HTTPException(404, "User not found")
    
    user_doc_data = user_doc.to_dict()
    user_doc_data = {key:val for key,val in user_doc_data.items() if key not in ('borrowed_books', 'waitlist')}

    # Get borrowed books
    user_doc_data['borrowed_books'] = get_borrowed_books(uid)

    # Get waitlist books
    user_doc_data['waitlist_books'] = get_waitlist(uid)

    return user_doc_data

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    user_pb2_grpc.add_UsersServicer_to_server(UserServer(), server)
    server.add_insecure_port('localhost:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
