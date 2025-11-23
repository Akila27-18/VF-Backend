import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from asgiref.sync import sync_to_async
from .models import ChatMessage


def now_time():
    return timezone.localtime().strftime("%I:%M %p")


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "global_chat_room"

        # Join WS group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Optional connect message
        await self.send_json({
            "type": "status",
            "data": {"message": "connected"}
        })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            payload = json.loads(text_data)
        except:
            return

        event_type = payload.get("type")
        data = payload.get("payload", {})

        # ----------------------------
        # 1️⃣ Handle Chat Message
        # ----------------------------
        if event_type == "message":
            from_user = data.get("from", "Anonymous")
            text = data.get("text", "")
            time_str = data.get("time") or now_time()

            # Save DB entry
            msg = await sync_to_async(ChatMessage.objects.create)(
                from_user=from_user,
                text=text,
                time=time_str
            )

            out = {
                "type": "message",
                "data": {
                    "id": str(msg.id),
                    "from_user": msg.from_user,
                    "text": msg.text,
                    "time": msg.time,
                    "created_at": msg.created_at.isoformat(),
                }
            }

            # Broadcast to all clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat.message", "message": out}
            )

            # Acknowledge sender
            await self.send_json({"type": "ack", "data": {"id": str(msg.id)}})

        # ----------------------------
        # 2️⃣ Typing Indicator
        # ----------------------------
        elif event_type == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat.typing", "message": {"from": data.get("from")}}
            )

        # ----------------------------
        # 3️⃣ Mark Seen
        # ----------------------------
        elif event_type == "mark_seen":
            ids = data.get("ids", [])
            if ids:
                await sync_to_async(ChatMessage.objects.filter(id__in=ids).update)(seen=True)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "chat.seen", "message": {"ids": ids}}
                )

    # ----------------------------
    # GROUP EVENTS
    # ----------------------------
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def chat_typing(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "data": event["message"]
        }))

    async def chat_seen(self, event):
        await self.send(text_data=json.dumps({
            "type": "seen",
            "data": event["message"]
        }))

    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))
