import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatMessage
from django.utils import timezone

def now_time():
    return timezone.localtime().strftime("%I:%M %p")

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "global_chat_room"

        # Join group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Optional: send connection status
        await self.send_json({"type": "status", "payload": {"message": "connected"}})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except:
            return

        event_type = data.get("type")
        payload = data.get("payload", {})

        # ------------------- Chat message -------------------
        if event_type == "chat":
            sender_name = payload.get("from", "Anonymous")
            text = payload.get("text", "")
            timestamp = payload.get("time") or now_time()

            # Save message to DB
            msg = await sync_to_async(ChatMessage.objects.create)(
                text=text,
                from_user=sender_name,
            )

            msg_data = {
                "id": str(msg.id),
                "from": sender_name,
                "text": text,
                "time": timestamp,
                "createdAt": msg.created_at.isoformat(),
            }

            # Broadcast to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "payload": msg_data}
            )

        # ------------------- Typing indicator -------------------
        elif event_type == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_typing", "payload": {"from": payload.get("from")}}
            )

    # ------------------- Group events -------------------
    async def chat_message(self, event):
        await self.send_json({"type": "chat", "payload": event["payload"]})

    async def chat_typing(self, event):
        await self.send_json({"type": "typing", "payload": event["payload"]})

    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))
