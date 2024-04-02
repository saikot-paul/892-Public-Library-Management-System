import grpc
import book_pb2
import book_pb2_grpc
import traceback
from google.protobuf import json_format
from fastapi import FastAPI
from pydantic import BaseModel


class DummyBook(BaseModel):
    Title: str
    Author: str
    Genre: str
    ISBN: str


class Book(DummyBook):
    Book_ID: int
    Status: bool


class id(BaseModel):
    Book_ID: int


class Checkout(BaseModel):
    user_id: str
    isbn: str

class ReturnBookData(BaseModel):
    user_id: str
    book_id: int


app = FastAPI()


@app.get("/books/search_isbn/{isbn}")
async def search_isbn(isbn: str):
    channel = grpc.insecure_channel('localhost:50051')
    stub = book_pb2_grpc.BooksStub(channel)

    request = book_pb2.ISBN(isbn_num=isbn)
    try:
        response = stub.SearchISBN(request)
        print("SearchISBN Response:", response)
        data = json_format.MessageToDict(response)
        empty = False if data else True

        return {
            "empty": empty,
            "data": data
        }

    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()


@app.get("/books/search_title/{title}")
async def search_title(title: str):
    channel = grpc.insecure_channel('localhost:50051')
    stub = book_pb2_grpc.BooksStub(channel)

    request = book_pb2.Title(title_str=title)
    try:
        response = stub.SearchTitle(request)
        print("SearchTitle Response:", response)
        data = json_format.MessageToDict(response)
        empty = False if data else True

        return {
            "empty": empty,
            "data": data
        }
    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()


@app.get("/books/search_genre/{genre}")
async def search_genre(genre: str):
    channel = grpc.insecure_channel('localhost:50051')
    stub = book_pb2_grpc.BooksStub(channel)

    request = book_pb2.Genre(genre_str=genre)
    try:
        response = stub.SearchGenre(request)
        print("SearchTitle Response:", response)

        data = json_format.MessageToDict(response)
        empty = False if data else True

        return {
            "empty": empty,
            "data": data
        }

    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()


@app.post("/books/create_book")
async def create_book(data: DummyBook):

    request = book_pb2.Book(
        title=data.Title,
        author=data.Author,
        genre=data.Genre,
        isbn=data.ISBN
    )

    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = book_pb2_grpc.BooksStub(channel)

        try:
            response = stub.CreateBook(request)
            print("CreateBook Response:", response)

            return json_format.MessageToJson(response)

        except grpc.RpcError as e:
            print(f"RPC failed with code {e.code()}: {e.details()}")
            traceback.print_exc()
    except Exception as e:
        print(f'Exception {e}')


@app.put("/books/update_book")
async def update_book(data: Book):

    request = book_pb2.UBook(
        title=data.Title,
        author=data.Author,
        genre=data.Genre,
        isbn=data.ISBN,
        book_id=data.Book_ID,
        status=data.Status
    )

    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = book_pb2_grpc.BooksStub(channel)

        response = stub.UpdateBook(request)
        print("CreateBook Response:", response)

        return json_format.MessageToJson(response)

    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()


@app.delete('/books/delete_book')
async def delete_book(id: id):

    request = book_pb2.BookID(book_id=id.Book_ID)

    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = book_pb2_grpc.BooksStub(channel)

        response = stub.DeleteBook(request)
        print("DeleteBook Response:", response)

        return json_format.MessageToJson(response)

    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()


@app.put('/books/checkout_book')
async def checkout_book(data: Checkout):

    request = book_pb2.CheckInfo(user_id=data.user_id, isbn=data.isbn)

    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = book_pb2_grpc.BooksStub(channel)

        response = stub.CheckoutBook(request)
        print("CheckoutBook Response:", response)

        print(json_format.MessageToJson(response))

    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()

@app.put('/books/return_book')
async def return_book(data: ReturnBookData):

    request = book_pb2.ReturnBookInfo(user_id=data.user_id, book_id=data.book_id)

    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = book_pb2_grpc.BooksStub(channel)

        response = stub.ReturnBook(request)
        print("ReturnBook Response:", response)

        print(json_format.MessageToJson(response))

    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()
