from django.db import models
from Auth.models import Auth
from Books.models import Book


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Auth, on_delete=models.CASCADE)
    borrow_at = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.borrower} - {self.book.title} - Paid: {self.is_paid}'
