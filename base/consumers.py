# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message,User , Room
from django.core.files.base import ContentFile
import base64
import uuid

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the room name from the URL kwargs
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(f"Connecting to room: {self.room_name}") 

        # Sanitize room name to ensure it's a valid group name
        self.room_name = self.room_name.replace(" ", "_")  # Replace spaces with underscores

        # Set the group name
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data ):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']  # New field to identify message type
        message_content = text_data_json['content']
        user = text_data_json['user']
        filename = text_data_json['filename']

        await self.save_message(message_content,message_type,user,self.room_name, filename)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_type': message_type,
                'content': message_content,
                'user': user
            }
        )

    async def chat_message(self, event):
        message_type = event['message_type']
        content = event['content']
        user = event['user']
        print(type(user))
        #print(content)
        #print(message_type)
        await self.send(text_data=json.dumps({
            'type': message_type,
            'content': content,
            'user': user
        }))

    @database_sync_to_async
    def save_message(self, content, message_type, user, room_name, filename=None):
        print(filename)
        user = User.objects.get(username=user)
        room = Room.objects.get(name=room_name.replace("_", " "))

        # Create a new message instance
        message = Message(
            user=user,
            room=room
        )

        # Set the message attributes based on the message type
        if message_type == 'text':
            message.body = content
        elif message_type in ['image', 'video', 'audio', 'file']:
            if ';base64,' in content:
                # Split the content by base64
                header, content_data = content.split(';base64,')
                content_type = header.split(':')[1].split(';')[0]

                # Decode the content
                file_data = base64.b64decode(content_data)

                if filename is None:  # Fallback if filename not provided
                    filename = f"attachment_{uuid.uuid4().hex}"

                if message_type == 'image':
                    message.image.save(filename, ContentFile(file_data))
                elif message_type == 'video':
                    message.video.save(filename, ContentFile(file_data))
                elif message_type == 'audio':
                    message.audio.save(filename, ContentFile(file_data))
                elif message_type == 'file':
                    print(filename)
                    message.file.save(filename, ContentFile(file_data))
        elif message_type == 'link':
            message.link = content

        # Save the message
        message.save()
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )