from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import  datetime
from.models import Room, Message
from channels.db import database_sync_to_async
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    @database_sync_to_async
    def get_room(self):
        return Room.objects.get(label=self.room_name)

    @database_sync_to_async
    def save_message(self, username, message):
        m = Message(room=self.room_object, username=username, message=message)
        return m.save()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        profile = text_data_json['profile']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'profile': profile
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        profile = event['profile']
        timestamp = datetime.datetime.now()

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username' : username,
            'profile' : profile,
            'timestamp' : timestamp.strftime('%y %m %d %H %M')

        }))