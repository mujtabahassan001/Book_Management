from rest_framework import viewsets, status

from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Auth.utils import JWTAuthentication
from Books.models import Book

from .models import Borrowing
from .serializer import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        borrowed_books = Borrowing.objects.all() 
        serializer = self.get_serializer(borrowed_books, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        action = request.data.get('action', None)  

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise NotFound({"error": "Book not found"})

        if action == 'return':
            try:
                borrowing = Borrowing.objects.get(book=book, borrower=request.user)
                borrowing.delete()  
                return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)
            except Borrowing.DoesNotExist:
                raise ValidationError({"error": "You have not borrowed this book."})

        if book.user == request.user:
            raise ValidationError({"error": "You cannot borrow your own book."})
        if Borrowing.objects.filter(book=book).exists():
            raise ValidationError({"error": "This book is already borrowed."})

        borrow = Borrowing.objects.create(book=book, borrower=request.user)
        serializer = self.get_serializer(borrow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)