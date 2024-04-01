# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import book_pb2 as book__pb2


class BooksStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SearchISBN = channel.unary_unary(
                '/books.Books/SearchISBN',
                request_serializer=book__pb2.ISBN.SerializeToString,
                response_deserializer=book__pb2.BookISBN.FromString,
                )
        self.SearchTitle = channel.unary_unary(
                '/books.Books/SearchTitle',
                request_serializer=book__pb2.Title.SerializeToString,
                response_deserializer=book__pb2.BookArray.FromString,
                )
        self.SearchGenre = channel.unary_unary(
                '/books.Books/SearchGenre',
                request_serializer=book__pb2.Genre.SerializeToString,
                response_deserializer=book__pb2.BookArray.FromString,
                )
        self.CreateBook = channel.unary_unary(
                '/books.Books/CreateBook',
                request_serializer=book__pb2.Book.SerializeToString,
                response_deserializer=book__pb2.Successful.FromString,
                )
        self.UpdateBook = channel.unary_unary(
                '/books.Books/UpdateBook',
                request_serializer=book__pb2.UBook.SerializeToString,
                response_deserializer=book__pb2.Successful.FromString,
                )
        self.DeleteBook = channel.unary_unary(
                '/books.Books/DeleteBook',
                request_serializer=book__pb2.BookID.SerializeToString,
                response_deserializer=book__pb2.Successful.FromString,
                )
        self.CheckoutBook = channel.unary_unary(
                '/books.Books/CheckoutBook',
                request_serializer=book__pb2.CheckInfo.SerializeToString,
                response_deserializer=book__pb2.Successful.FromString,
                )
        self.ReturnBook = channel.unary_unary(
                '/books.Books/ReturnBook',
                request_serializer=book__pb2.ReturnBookInfo.SerializeToString,
                response_deserializer=book__pb2.Successful.FromString,
                )
        self.WaitlistBook = channel.unary_unary(
                '/books.Books/WaitlistBook',
                request_serializer=book__pb2.CheckInfo.SerializeToString,
                response_deserializer=book__pb2.Successful.FromString,
                )


class BooksServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SearchISBN(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchTitle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchGenre(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateBook(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateBook(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteBook(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckoutBook(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReturnBook(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WaitlistBook(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BooksServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SearchISBN': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchISBN,
                    request_deserializer=book__pb2.ISBN.FromString,
                    response_serializer=book__pb2.BookISBN.SerializeToString,
            ),
            'SearchTitle': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchTitle,
                    request_deserializer=book__pb2.Title.FromString,
                    response_serializer=book__pb2.BookArray.SerializeToString,
            ),
            'SearchGenre': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchGenre,
                    request_deserializer=book__pb2.Genre.FromString,
                    response_serializer=book__pb2.BookArray.SerializeToString,
            ),
            'CreateBook': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateBook,
                    request_deserializer=book__pb2.Book.FromString,
                    response_serializer=book__pb2.Successful.SerializeToString,
            ),
            'UpdateBook': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateBook,
                    request_deserializer=book__pb2.UBook.FromString,
                    response_serializer=book__pb2.Successful.SerializeToString,
            ),
            'DeleteBook': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteBook,
                    request_deserializer=book__pb2.BookID.FromString,
                    response_serializer=book__pb2.Successful.SerializeToString,
            ),
            'CheckoutBook': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckoutBook,
                    request_deserializer=book__pb2.CheckInfo.FromString,
                    response_serializer=book__pb2.Successful.SerializeToString,
            ),
            'ReturnBook': grpc.unary_unary_rpc_method_handler(
                    servicer.ReturnBook,
                    request_deserializer=book__pb2.ReturnBookInfo.FromString,
                    response_serializer=book__pb2.Successful.SerializeToString,
            ),
            'WaitlistBook': grpc.unary_unary_rpc_method_handler(
                    servicer.WaitlistBook,
                    request_deserializer=book__pb2.CheckInfo.FromString,
                    response_serializer=book__pb2.Successful.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'books.Books', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Books(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SearchISBN(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/books.Books/SearchISBN',
            book__pb2.ISBN.SerializeToString,
            book__pb2.BookISBN.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SearchTitle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/books.Books/SearchTitle',
            book__pb2.Title.SerializeToString,
            book__pb2.BookArray.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SearchGenre(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/books.Books/SearchGenre',
            book__pb2.Genre.SerializeToString,
            book__pb2.BookArray.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateBook(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/books.Books/CreateBook',
            book__pb2.Book.SerializeToString,
            book__pb2.Successful.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateBook(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/books.Books/UpdateBook',
            book__pb2.UBook.SerializeToString,
            book__pb2.Successful.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteBook(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/books.Books/DeleteBook',
            book__pb2.BookID.SerializeToString,
            book__pb2.Successful.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckoutBook(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/books.Books/CheckoutBook',
            book__pb2.CheckInfo.SerializeToString,
            book__pb2.Successful.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReturnBook(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/books.Books/ReturnBook',
            book__pb2.ReturnBookInfo.SerializeToString,
            book__pb2.Successful.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def WaitlistBook(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/books.Books/WaitlistBook',
            book__pb2.CheckInfo.SerializeToString,
            book__pb2.Successful.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
