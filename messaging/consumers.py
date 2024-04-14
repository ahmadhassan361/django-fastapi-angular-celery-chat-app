import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from app.auth.auth_handler import decodeJWT
from urllib.parse import parse_qs
from django.contrib.auth.models import User
from .models import ChatRoom, ChatRoomParticipant
from .tasks import send_message_emails

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Accessing headers to retrieve JWT
        query_params = parse_qs(self.scope["query_string"].decode())
        token = query_params.get("token", [None])[0]
        if not token:
            # Token not found or invalid
            self.close()
            return

        # Decode JWT token
        decoded_token = decodeJWT(token)
        if not decoded_token:
            # Invalid token
            self.close()
            return
        
        # Retrieve user based on decoded token
        user = User.objects.get(username=decoded_token['user_id'])
        self.user = user
        
        # Try to find the room or create it if it doesn't exist
        self.room, created = ChatRoom.objects.get_or_create(name=self.room_name)
        
        # Add user to the room
        participant, _ = ChatRoomParticipant.objects.get_or_create(user=self.user, room=self.room)
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        json_text = json.loads(text_data)
        message = json_text["message"]
        
        # Send message to room group    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "user": self.user.username  # Send the username of the sender
            }
        )
        
        # Trigger Celery task to send emails to room users
        send_message_emails.delay(self.room_name, message)

    def chat_message(self, event):
        message = event["message"]
        username = event["user"]  # Get the username from the event

        # Send message to WebSocket with username
        self.send(text_data=json.dumps({
            "message": message,
            "user": username  # Send the username received from the event
        }))
