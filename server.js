// backend/server.js
import express from "express";
import { WebSocketServer } from "ws";
import http from "http";
import cors from "cors";

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

// ---------------- Stock API (mock/Yahoo API example) ----------------
app.get("/api/stock/:symbol", async (req, res) => {
  const { symbol } = req.params;

  // Replace with real stock fetching logic if needed
  const mockData = {
    chart: {
      result: [
        {
          indicators: {
            quote: [
              { close: Array.from({ length: 20 }, () => 100 + Math.random() * 50) },
            ],
          },
        },
      ],
    },
  };

  res.json(mockData);
});

// ---------------- HTTP + WebSocket Server ----------------
const server = http.createServer(app);

// WebSocket server for chat
const wss = new WebSocketServer({ server, path: "/ws/chat/" });
console.log(`WebSocket server mounted on ws://localhost:${PORT}/ws/chat/`);

wss.on("connection", (ws) => {
  console.log("Client connected");

  ws.on("message", (msg) => {
    let data;
    try {
      data = JSON.parse(msg);
    } catch (err) {
      console.error("Invalid JSON", err);
      return;
    }

    // Broadcast to all clients except sender
    wss.clients.forEach((client) => {
      if (client !== ws && client.readyState === ws.OPEN) {
        client.send(JSON.stringify(data));
      }
    });
  });

  ws.on("close", () => console.log("Client disconnected"));
});

// ---------------- Start server ----------------
server.listen(PORT, () => {
  console.log(`Express API running on http://localhost:${PORT}`);
});
