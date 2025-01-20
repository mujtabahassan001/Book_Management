from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Auth.utils import JWTAuthentication
from Books.models import Book
from .models import Borrowing
from .serializer import BorrowingSerializer
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("SECRET_KEY")

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

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=1000,
                currency='usd',
                automatic_payment_methods={
                'enabled': True,
                'allow_redirects': 'never'  
            },
                description=f'Borrowing fee for {book.title}',
            )
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        borrow = Borrowing.objects.create(
            book=book,
            borrower=request.user,
            stripe_payment_intent_id=payment_intent.id
        )
        serializer = self.get_serializer(borrow)

        return Response({
            "borrowing": serializer.data,
            "payment_intent": payment_intent.client_secret
        }, status=status.HTTP_201_CREATED)

    def confirm_payment(self, request, *args, **kwargs):
        borrowing_id = kwargs.get("pk")
        payment_intent_id = request.data.get("payment_intent_id")

        try:
            borrowing = Borrowing.objects.get(id=borrowing_id)
        except Borrowing.DoesNotExist:
            raise NotFound({"error": "Borrowing record not found"})

        if borrowing.stripe_payment_intent_id != payment_intent_id:
            raise ValidationError({"error": "Payment intent ID mismatch"})

        try:
            payment_method = stripe.PaymentMethod.create(
                type='card',
                card={'token': 'tok_visa'}  
            )

            stripe.PaymentIntent.modify(
                payment_intent_id,
                payment_method=payment_method.id
            )

            payment_intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                off_session=True  
            )

            if payment_intent.status == 'succeeded':
                borrowing.is_paid = True
                borrowing.save()
                return Response({
                    "status": "Payment confirmed and borrowing updated",
                    "payment_status": payment_intent.status
                })
            else:
                return Response({
                    "error": f"Payment failed with status: {payment_intent.status}"
                }, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
