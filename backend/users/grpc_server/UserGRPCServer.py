import user_pb2
import user_pb2_grpc
import firestore_db
from firestore_db import db
from firebase_admin import firestore
from concurrent import futures
import grpc

from router.borrowed_books import *
from router.waitlist import *
from router.recommendations import *
from router.user_crud import *

class UserServer(user_pb2_grpc.UsersServicer):
    def GetBorrowedBooks(self, request, context):
        uid = request.uid

        borrowed_books = get_borrowed_books(uid)

        all_books_response = user_pb2.AllBooksMessage()
        all_books_response.books.extend([])

        for book in borrowed_books:
            # Get book data
            bb_data = book.to_dict()
            book_data = bb_data['all_books_doc_ref'].get().to_dict()
            book_data = {key.lower(): value for key, value in book_data.items()}

            book_message = user_pb2.AllBooksBook(
                title = book_data.get('title', ''),
                borrowed_by = book_data.get('borrowed_by', ''),
                genre = book_data.get('genre', ''),
                status = book_data.get('status', None),
                keywords = book_data.get('keywords', []),
                author = book_data.get('author', ''),
                book_id = book_data.get('book_id', -1),
                isbn = book_data.get('isbn', '')
            )

            all_books_response.books.append(book_message)
        
        all_books_response.success = True
        all_books_response.message = 'Borrowed books retrieved.'
        return all_books_response
    
    def GetRecommendations(self, request, context):
        uid = request.uid

        try:
            recommendations = get_recommendations(uid)
        except Exception as e:
            return user_pb2.FilteredBooksMessage(
                success = False,
                books = [],
                message = repr(e)
            )

        print(recommendations)

        # Form response
        filtered_books_res = user_pb2.FilteredBooksMessage()
        filtered_books_res.books.extend([])

        for r in recommendations:
            filtered_book = user_pb2.FilteredBooksBook(
                title = r.get('title', ''),
                checkout_list = r.get('checkout_list', []),
                genre = r.get('genre', ''),
                status = r.get('status', None),
                keywords = r.get('keywords', []),
                author = r.get('author', ''),
                isbn = r.get('isbn', ''),
                available_copies = r.get('available_copies', -1),
                num_copies = r.get('num_copies', -1)
            )

            filtered_books_res.books.append(filtered_book)

        filtered_books_res.success = True
        filtered_books_res.message = "Retrieved recommendations successfully."
        return filtered_books_res

    # Note that if num_copies and available_copies are not found as fields in the waitlisted books, they are 0.
    # In proto3, explicit default values are not allowed, and the default value of an int32 is 0.
    def GetWaitlist(self, request, context):
        uid = request.uid

        try:
            waitlist = get_waitlist(uid)
        except Exception as e:
            return user_pb2.FilteredBooksMessage(
                success = False,
                books = [],
                message = repr(e)
            )

        # Form response
        filtered_books_res = user_pb2.FilteredBooksMessage()
        filtered_books_res.books.extend([])

        for book in waitlist:
            filtered_book = user_pb2.FilteredBooksBook(
                title = book.get('title', ''),
                checkout_list = book.get('checkout_list', []),
                genre = book.get('genre', ''),
                status = book.get('status', None),
                keywords = book.get('keywords', []),
                author = book.get('author', ''),
                isbn = book.get('isbn', ''),
                available_copies = book.get('available_copies', -1),
                num_copies = book.get('num_copies', -1)
            )

            filtered_books_res.books.append(filtered_book)

        return filtered_books_res

    def AppendToWaitlist(self, request, context):
        uid = request.uid
        isbn = request.isbn

        try:
            ret_val = append_to_waitlist(uid, isbn)
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
            message = ret_val['message']
        )

    def DeleteFromWaitlist(self, request, context):

        uid = request.uid
        isbn = request.isbn

        try:
            ret_val = delete_from_waitlist(uid, isbn)
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
            message = ret_val['message']
        )

    def GetUserInfo(self, request, context):
        uid = request.uid

        print("GetUserInfo: ", uid)

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

        print(user_info_data)

        user_info_msg = user_pb2.UserInfo(
            first_name = user_info_data.get('first_name', ''),
            last_name = user_info_data.get('last_name', ''),
            contact_number = user_info_data.get('contact_number', ''),
            postal_code = user_info_data.get('postal_code', ''),
            email = user_info_data.get('email', '')
        )

        if 'waitlist_books' in user_info_data:
            user_info_msg.waitlist_books.extend([])

            for book in user_info_data['waitlist_books']:
                filtered_book = user_pb2.FilteredBooksBook(
                    title = book.get('title', ''),
                    checkout_list = book.get('checkout_list', []),
                    genre = book.get('genre', ''),
                    status = book.get('status', None),
                    keywords = book.get('keywords', []),
                    author = book.get('author', ''),
                    isbn = book.get('isbn', ''),
                    available_copies = book.get('available_copies', -1),
                    num_copies = book.get('num_copies', -1)
                )
                user_info_msg.waitlist_books.append(filtered_book)

        if 'borrowed_books' in user_info_data:
            user_info_msg.borrowed_books.extend([])

            for book in user_info_data['borrowed_books']:
                book_message = user_pb2.AllBooksBook(
                    title = book.get('title', ''),
                    borrowed_by = book.get('borrowed_by', ''),
                    genre = book.get('genre', ''),
                    status = book.get('status', None),
                    keywords = book.get('keywords', []),
                    author = book.get('author', ''),
                    book_id = book.get('book_id', -1),
                    isbn = book.get('isbn', '')
                )
                user_info_msg.borrowed_books.append(book_message)

        return user_pb2.UserInfoMessage(
            success = True,
            user_info = user_info_msg,
            message = f"Retrieved {uid} info successfully."
        )

    def UpdateUserInfo(self, request, context):
        req_data = {field.name: getattr(request, field.name) for field in request.DESCRIPTOR.fields}

        update_data = {key:val for key,val in req_data.items() if key != 'uid'}

        db.document(f"users/{req_data['uid']}").update(update_data)

        return user_pb2.SimpleMessage(
            success = True,
            message = f"Successfully updated {req_data.get('uid')} info"
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    user_pb2_grpc.add_UsersServicer_to_server(UserServer(), server)
    server.add_insecure_port('localhost:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
