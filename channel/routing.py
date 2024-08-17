from django.urls import path
from channel.consumers import MyWebsocketConsumer

webscoket_urlpatterns = [
    path('ws/wsc/<str:groupname>',MyWebsocketConsumer.as_asgi())
]