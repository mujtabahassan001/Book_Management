from rest_framework import serializers
from Auth.serializer import LoginSerializer

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    user= LoginSerializer(read_only=True)

    class Meta:
        model= Book
        fields= ['id', 'title', 'author', 'pages', 'price', 'user']
        read_only_fields= ['user']
