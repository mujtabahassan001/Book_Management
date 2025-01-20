from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BorrowingViewSet

router = DefaultRouter()
router.register(r'borrowing', BorrowingViewSet, basename='borrowing')

urlpatterns = router.urls + [
    path('borrowing/<int:pk>/confirm_payment/', BorrowingViewSet.as_view({'post': 'confirm_payment'}), name='confirm_payment'),
]