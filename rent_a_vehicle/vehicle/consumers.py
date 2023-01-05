import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core import serializers
from vehicle.models import RentedLogs


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close(code=404)
        self.user = self.scope["url_route"]["kwargs"]["user"]
        self.user_group_name = "notification_%s" % self.user
        pending_rent_request = await sync_to_async(list)(RentedLogs.objects.filter(request_status='pending'))
        serializer = serializers.serialize('json', pending_rent_request)

        await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        await self.accept()
        await self.send(json.dumps({
            'type': 'websocket.send',
            'response': json.loads(serializer)
        }))

    async def disconnect(self, close_code):
        if hasattr(NotificationConsumer, 'room_group_name') and hasattr(NotificationConsumer, 'channel_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data = json.loads(text_data)
        await sync_to_async(RentedLogs.objects.update_or_create, thread_sensitive=True)(id=text_data['vehicle'], defaults={'request_status':text_data['request_status']})

    async def send_owner_notification(self, event):
        await self.send(text_data=json.dumps({'payload': json.loads(event.get('value'))}))

    async def send_renter_notification(self, event):
        await self.send(text_data=json.dumps({'payload': event.get('value')}))
