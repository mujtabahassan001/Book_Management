from rest_framework import serializers

from .models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    borrower = serializers.CharField(source='borrower.email', read_only=True)  
    
    class Meta:
        model= Borrowing
        fields= ['id','book','borrower','borrow_at']
        read_only_fields= ['borrower','borrow_at']