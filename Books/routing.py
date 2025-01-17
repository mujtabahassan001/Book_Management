from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/books/$', consumers.BookConsumer.as_asgi()),
]