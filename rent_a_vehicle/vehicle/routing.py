from django.urls import path

from . import consumers

ws_router = [
    path("ws/notification/<int:user>", consumers.NotificationConsumer.as_asgi()),
]
