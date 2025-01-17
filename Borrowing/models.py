from django.db import models
from Books.models import Book
from Auth.models import Auth



class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower= models.ForeignKey(Auth, on_delete=models.CASCADE)
    borrow_at= models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f'{self.borrower} - {self.book.title}'