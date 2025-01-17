from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_book_notification(action, book_title, username):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'book_notifications',
        {
            'type': 'book_notification',
            'message': f'{username} {action} book: {book_title}'
        }
    )
