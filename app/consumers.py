# app/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime

class NewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "news_room"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Optional connection message
        await self.send_json({"type": "status", "data": {"message": "connected"}})

        # Start sending mock news updates
        asyncio.create_task(self.send_news_updates())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_news_updates(self):
        while True:
            news = [
                {
                    "id": 1,
                    "title": "Markets stable",
                    "summary": f"Equity markets saw moderate gains at {datetime.now().strftime('%H:%M:%S')}."
                },
                {
                    "id": 2,
                    "title": "Interest rate update",
                    "summary": f"RBI keeps repo rate unchanged at {datetime.now().strftime('%H:%M:%S')}."
                }
            ]
            await self.send_json({"type": "news_update", "data": news})
            await asyncio.sleep(15)  # every 15s

    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))
