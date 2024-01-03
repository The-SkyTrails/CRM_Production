from . import consumers
from django.urls import path, re_path

websocket_urlpatterns = [
    path("wss/chat/<str:group_id>/", consumers.ChatConsumer.as_asgi()),
]
