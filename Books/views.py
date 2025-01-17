from rest_framework import status, viewsets

from Auth.utils import JWTAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializer import BookSerializer
from .models import Book
from .notification import send_book_notification


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):
        queryset = Book.objects.filter(user=request.user).order_by('title') 
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            send_book_notification(
                'created',
                serializer.data['title'],
                request.user.username
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            if book.user != request.user:
                raise PermissionDenied("You don't have permission to access this book")
            serializer = self.serializer_class(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found")
    
    def update(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            if book.user != request.user:
                raise PermissionDenied("You don't have permission to modify this book")
            
            serializer = self.serializer_class(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                send_book_notification(
                    'updated',
                    serializer.data['title'],
                    request.user.username
                )
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found")
        
    def destroy(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            if book.user != request.user:
                raise PermissionDenied("You don't have permission to delete this book")
            
            title = book.title  
            book.delete()
            send_book_notification(
                'deleted',
                title,
                request.user.username
            )
            return Response(
                {"message": "Book deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found")

    def partial_update(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            if book.user != request.user:
                raise PermissionDenied("You don't have permission to modify this book")
            
            serializer = self.serializer_class(
                book,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                send_book_notification(
                    'updated',
                    serializer.data['title'],
                    request.user.username
                )
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found")