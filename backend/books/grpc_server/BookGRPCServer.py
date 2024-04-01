import book_pb2
import book_pb2_grpc
import firestore_db
from firestore_db import db
from firebase_admin import firestore
from concurrent import futures
import grpc
import traceback
from datetime import datetime

class BookServer(book_pb2_grpc.BooksServicer):

    """
    This class is a gRPC server where it solely communicates with the books database 
    """

    def SearchISBN(self, request, context):
        """
        Searches for books using the isbn 
        """
        isbn = request.isbn_num
        print(f'Called SearchISBN: {isbn}')
        print(isbn)

        doc_ref = db.collection('filtered_books').document(isbn)
        doc = doc_ref.get()
        data = doc.to_dict()
        print(data)

        if doc.exists:
            book = book_pb2.BookSearch(
                title=data.get('Title', ''),
                checkout_list=data.get('checkout_list', [" "]),
                genre=data.get('Genre', ''),
                keywords=data.get('Keywords', [" "]),
                author=data.get('Author', ''),
                available_copies=data.get('available_copies', 0),
                num_copies=data.get('num_copies', 0)
            )
            return book_pb2.BookISBN(empty=False, book=book)

        return book_pb2.BookISBN(empty=True)

    def SearchTitle(self, request, context):

        title_arr = request.title_str.split("+")
        print(f'Called SearchTitle: {title_arr}')
        title_arr = [item.capitalize() for item in title_arr]
        query_ref = db.collection('filtered_books').where(
            'Keywords', 'array_contains_any', title_arr)

        docs = query_ref.stream()

        if docs:
            books = []
            for res in docs:
                data = res._data
                book = book_pb2.BookSearch(
                    title=data.get('Title', ''),
                    checkout_list=data.get('checkout_list', [" "]),
                    genre=data.get('Genre', ''),
                    keywords=data.get('Keywords', [" "]),
                    author=data.get('Author', ''),
                    available_copies=data.get('available_copies', 0),
                    num_copies=data.get('num_copies', 0)
                )

                books.append(book)

            return book_pb2.BookArray(books=books)

        return book_pb2.BookArray()

    def SearchGenre(self, request, context):

        genre = request.genre_str

        gen = genre.capitalize()
        print(f'Called SearchGenre: {gen}')
        query_ref = db.collection('filtered_books').where(
            'Genre', '==', gen)

        docs = query_ref.stream()

        if docs:
            books = []
            for res in docs:
                data = res._data
                book = book_pb2.BookSearch(
                    title=data.get('Title', ''),
                    checkout_list=data.get('checkout_list', [" "]),
                    genre=data.get('Genre', ''),
                    keywords=data.get('Keywords', [" "]),
                    author=data.get('Author', ''),
                    available_copies=data.get('available_copies', 0),
                    num_copies=data.get('num_copies', 0)
                )

                books.append(book)

            return book_pb2.BookArray(books=books)

        return book_pb2.BookArray()

    def CreateBook(self, request, context):

        print(f'Called CreateBook: {request}')
        filtered_data = {
            'Title': request.title,
            'Author': request.author,
            'Genre': request.genre,
            'ISBN': request.isbn,
            'Keywords': request.title.split(" ")
        }

        docs = db.collection('all_books').get()

        count = -1
        for res in docs:

            curr = res._data['Book_ID']
            count = max(count, curr)

        count += 1

        book_data = filtered_data.copy()
        book_data["Book_ID"] = count
        book_data['Status'] = False

        isbn = filtered_data['ISBN']

        filtered_data['num_copies'] = 1
        filtered_data['available_copies'] = 1
        filtered_data['checkout_list'] = []

        db.collection('all_books').document().set(book_data)

        doc_ref = db.collection('filtered_books').document(request.isbn)
        doc = doc_ref.get()

        print(doc._data)
        print(doc._exists)

        if not doc._exists:
            db.collection('filtered_books').document(isbn).set(filtered_data)
        else:
            data = doc._data
            data['num_copies'] += 1
            data['available_copies'] += 1
            doc_ref.update(data)

        return book_pb2.Successful(ack=True)

    def UpdateBook(self, request, context):
        print(f'Called CreateBook: {request}')
        data = {
            'Title': request.title,
            'Author': request.author,
            'Genre': request.genre,
            'ISBN': request.isbn,
            'Keywords': request.title.split(" "),
            'Book_ID': request.book_id,
            'Status': request.status
        }

        book_id = data['Book_ID']

        query_ref = db.collection('all_books').where(
            'Book_ID', '==', book_id
        )

        doc = list(query_ref.stream())[0]

        if doc.exists:
            data = doc._data

            doc_ref = db.collection('filtered_books').document(data['ISBN'])
            doc = doc_ref.get()
            filtered_data = doc.to_dict()
            if data['Status']:
                filtered_data['available_copies'] -= 1

            doc_ref.update({
                'Title': request.title,
                'Author': request.author,
                'Genre': request.genre,
                'Keywords': request.title.split(" "),
                'available_copies': data['available_copies']
            })

            db.collection('all_books').document(doc.id).update(data)
            return book_pb2.Successful(ack=True)

        return book_pb2.Successful(ack=False)

    def DeleteBook(self, request, context):

        id = request.book_id

        query_ref = db.collection('all_books').where('Book_ID', '==', id)
        docs = query_ref.stream()

        for res in docs:
            data = res._data

            doc_ref = db.collection('filtered_books').document(data['ISBN'])
            doc = doc_ref.get()
            filter_data = doc.to_dict()

            filter_data['available_copies'] -= 1
            filter_data['num_copies'] -= 1

            doc_ref.update(filter_data)
            db.collection('all_books').document(res.id).delete()

            return book_pb2.Successful(ack=True)

        return book_pb2.Successful(ack=False)

    def CheckoutBook(self, request, context):

        uid = request.user_id
        isbn = request.isbn

        doc_ref = db.collection('filtered_books').document(isbn)
        doc = doc_ref.get()

        if (doc.exists):
            print("Book exists")
            data = doc.to_dict()
            if (data['available_copies'] >= 1):
                print("available copies: ", data['available_copies'])
                data['available_copies'] -= 1
                data['checkout_list'].append(uid)
                doc_ref.update(data)

                query_ref = db.collection(
                    'all_books').where('ISBN', '==', isbn)
                books = query_ref.stream()

                for b in books:
                    b_data = b._data
                    if not b_data['Status']:
                        print("doc id of book", b.id)
                        # Found a book with matching ISBN that has not been borrowed
                        db.collection('all_books').document(b.id).update({
                            "Status": True
                        })

                        # Add book to user's borrowed book collection
                        print(f'/users/{uid}/borrowed_books/{b.id}')
                        db.document(f'/users/{uid}/borrowed_books/{b.id}').set({
                            'isbn': isbn,
                            'book_doc_ref': db.document(f'/all_books/{isbn}'),
                            'borrow_date': datetime.now()
                        })

                        return book_pb2.Successful(ack=True, message=f"Successfully checked out book with isbn {isbn}")
            else:
                print("no copies found")
                return book_pb2.Successful(ack=False, message=f"No copies of {isbn} available for checkout")
        else:
            return book_pb2.Successful(ack=False, message=f"Book with {isbn} not found")
        
        return book_pb2.Successful(ack=False, message=f"Unable to complete request")
    
    def WaitlistBook(self, request, context):
        
        # Get book's reference and data
        ubook_doc_ref = db.collection('filtered_books').document(request.isbn)
        ubook_doc = ubook_doc_ref.get()

        if not ubook_doc.exists:
            return book_pb2.Successful(ack=False, message=f"Unique book with isbn {request.isbn} cannot be found")
        
        ubook_data = ubook_doc.to_dict()

        # Create doc in user's waitlisted_books collection
        db.document(f'users/{request.user_id}/waitlisted_books/{request.isbn}').set({
            'filtered_books_ref': db.document(f'filtered_books/{request.isbn}'),
            'isbn': request.isbn,
            'title': ubook_data.get('title'),
            'waitlist_date': datetime.now()
        })
    
        # Add the user to the unique book's waitlist array
        if 'waitlist' in ubook_data:
            ubook_data['waitlist'].append(request.user_id)
        else:
            ubook_data['waitlist'] = [request.user_id]
        ubook_doc_ref.update({'waitlist': ubook_data['waitlist']})

        return book_pb2_grpc.Successful(ack=False, message=f"User {request.user_id} has been added to book {request.isbn} waitlist")

    def get_books_by_isbn(self, isbn: str):
        """
        Helper function to get a list of books with the same isbn
        """
        query_ref = db.collection('filtered_books').where(
            'ISBN', '==', isbn, )

        docs = query_ref.stream()

        data = [res._data for res in docs]

        return data


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    book_pb2_grpc.add_BooksServicer_to_server(BookServer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
