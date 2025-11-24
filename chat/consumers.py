import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from asgiref.sync import sync_to_async
from .models import ChatMessage, Expense
from django.contrib.auth.models import User


def now_time():
    return timezone.localtime().strftime("%I:%M %p")


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "global_chat_room"

        # Join room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Optional: send initial connected message
        await self.send_json({"type": "status", "data": {"message": "connected"}})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            return

        event_type = payload.get("type")
        data = payload.get("payload", {})

        # ----------------------------
        # 1️⃣ Handle chat message
        # ----------------------------
        if event_type == "message":
            sender_username = data.get("from", "Anonymous")
            text = data.get("text", "")
            time_str = data.get("time") or now_time()

            # Optional: link to expense
            expense_id = data.get("expense_id")
            expense = None
            if expense_id:
                try:
                    expense = await sync_to_async(Expense.objects.get)(id=expense_id)
                except Expense.DoesNotExist:
                    expense = None

            # Save to DB
            msg = await sync_to_async(ChatMessage.objects.create)(
                sender=await sync_to_async(User.objects.get)(username=sender_username),
                receiver=None,  # global chat; can be enhanced for private
                text=text,
                expense=expense
            )

            out = {
                "type": "message",
                "data": {
                    "id": str(msg.id),
                    "from": sender_username,
                    "text": msg.text,
                    "time": time_str,
                    "created_at": msg.created_at.isoformat(),
                    "expense_id": expense.id if expense else None
                }
            }

            # Broadcast to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat.message", "message": out}
            )

            # Acknowledge sender
            await self.send_json({"type": "ack", "data": {"id": str(msg.id)}})

        # ----------------------------
        # 2️⃣ Typing indicator
        # ----------------------------
        elif event_type == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat.typing", "message": {"from": data.get("from")}}
            )

        # ----------------------------
        # 3️⃣ Mark seen
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
    # Group events
    # ----------------------------
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def chat_typing(self, event):
        await self.send(text_data=json.dumps({"type": "typing", "data": event["message"]}))

    async def chat_seen(self, event):
        await self.send(text_data=json.dumps({"type": "seen", "data": event["message"]}))

    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))
