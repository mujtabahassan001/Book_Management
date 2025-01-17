from Auth.models import Auth
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    pages = models.IntegerField()
    price = models.FloatField()
    user= models.ForeignKey(Auth, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title + '-' + self.price