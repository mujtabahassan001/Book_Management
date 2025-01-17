from rest_framework.routers import DefaultRouter

from .views import BorrowingViewSet


router= DefaultRouter()
router.register(r'borrowing', BorrowingViewSet, basename= 'borrowing')

urlpatterns = router.urls
