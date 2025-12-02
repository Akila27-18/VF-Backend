# backend/chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "global_chat_room"

        # Join group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Optional: notify client
        await self.send_json({"type": "status", "data": {"message": "connected"}})

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return

        try:
            payload = json.loads(text_data)
        except Exception:
            return

        typ = payload.get("type")
        pl = payload.get("payload", {})

        user = self.scope["user"]
        if not user.is_authenticated:
            await self.send_json({"type": "error", "data": "Authentication required"})
            return

        if typ == "message":
            text = pl.get("text", "")

            # Save message
            msg = ChatMessage.objects.create(sender=user, text=text)

            out = {
                "type": "message",
                "data": {
                    "id": msg.id,
                    "from_user": user.username,
                    "text": msg.text,
                    "created_at": msg.created_at.isoformat(),
                }
            }

            # Broadcast to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat.message", "message": out}
            )

            # Optional ack to sender
            await self.send_json({"type": "ack", "data": {"id": msg.id}})

        elif typ == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.typing",
                    "message": {"from_user": user.username}
                }
            )

        elif typ == "mark_seen":
            ids = pl.get("ids", [])
            if ids:
                ChatMessage.objects.filter(id__in=ids).update(seen=True)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "chat.seen", "message": {"ids": ids}}
                )

    # Handlers for group_send events
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def chat_typing(self, event):
        await self.send(text_data=json.dumps({"type": "typing", "data": event["message"]}))

    async def chat_seen(self, event):
        await self.send(text_data=json.dumps({"type": "seen", "data": event["message"]}))
