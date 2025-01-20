from rest_framework import serializers
from .models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    borrower = serializers.CharField(source='borrower.email', read_only=True)  

    class Meta:
        model = Borrowing
        fields = ['id', 'book', 'borrower', 'borrow_at', 'stripe_payment_intent_id', 'is_paid']
        read_only_fields = ['borrower', 'borrow_at', 'stripe_payment_intent_id', 'is_paid']
