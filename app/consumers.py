# app/consumers.py

import json
import asyncio
from datetime import datetime
from django.utils import timezone
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatMessage


#------------------------- Helpers -------------------------
def now_time():
    return timezone.localtime().strftime("%I:%M %p")


#------------------------- Chat Consumer -------------------------
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "global_chat_room"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.send_json({
            "type": "status",
            "data": {"message": "connected"}
        })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            data = json.loads(text_data)
        except:
            return

        event_type = data.get("type")
        payload = data.get("payload", {})

        # -------- Chat messages --------
        if event_type == "message":
            sender = self.scope["user"]
            if not sender.is_authenticated:
                return

            text = payload.get("text", "")
            receiver_id = payload.get("receiver_id")

            if not receiver_id or not text:
                return

            msg = await sync_to_async(ChatMessage.objects.create)(
                sender=sender,
                receiver_id=receiver_id,
                text=text,
                created_at=timezone.now()
            )

            out = {
                "type": "message",
                "data": {
                    "id": msg.id,
                    "from_user": sender.username,
                    "to_user": receiver_id,
                    "text": text,
                    "time": now_time(),
                    "created_at": msg.created_at.isoformat()
                }
            }

            # broadcast to all
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": out
                }
            )

            await self.send_json({"type": "ack", "data": {"id": msg.id}})

        # -------- Typing indicators --------
        elif event_type == "typing":
            from_user = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.typing",
                    "message": {"from": from_user}
                }
            )

    async def chat_message(self, event):
        await self.send_json(event["message"])

    async def chat_typing(self, event):
        await self.send_json({"type": "typing", "data": event["message"]})

    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))


#------------------------- News Consumer -------------------------
class NewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "news_room"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        self.news_task = asyncio.create_task(self.send_news_updates())

        await self.send_json({
            "type": "status",
            "data": {"message": "connected"}
        })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if hasattr(self, "news_task"):
            self.news_task.cancel()

    async def send_news_updates(self):
        try:
            while True:
                news = [
                    {
                        "id": 1,
                        "title": "Markets stable",
                        "summary": f"Equity markets saw gains at {datetime.now().strftime('%H:%M:%S')}."
                    },
                    {
                        "id": 2,
                        "title": "Interest rate update",
                        "summary": f"RBI keeps repo rate unchanged at {datetime.now().strftime('%H:%M:%S')}."
                    }
                ]

                await self.send_json({
                    "type": "news_update",
                    "data": news
                })

                await asyncio.sleep(15)

        except asyncio.CancelledError:
            pass

    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))


#------------------------- Dashboard Consumer -------------------------
class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_json({
            "type": "status",
            "data": {"message": "Dashboard WebSocket connected"}
        })

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        # Echo back as proper JSON wrapper
        try:
            data = json.loads(text_data)
        except:
            data = {"raw": text_data}

        await self.send_json({"type": "echo", "data": data})

    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))
