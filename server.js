import express from "express";
import { WebSocketServer } from "ws";
import http from "http";
import cors from "cors";

const app = express();
const PORT = process.env.PORT || 5000; // Use Render port

// CORS for frontend domain
app.use(cors({
  origin: "https://vf-frontend.onrender.com",
  credentials: true
}));
app.use(express.json());

// ---------------- Stock API (mock example) ----------------
app.get("/api/stock/:symbol", async (req, res) => {
  const { symbol } = req.params;

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
const wss = new WebSocketServer({ server, path: "/ws/chat/" });

wss.on("connection", (ws) => {
  console.log("WS client connected");

  ws.on("message", (msg) => {
    let data;
    try {
      data = JSON.parse(msg);
    } catch (err) {
      console.error("Invalid JSON", err);
      return;
    }

    // Broadcast to all except sender
    wss.clients.forEach((client) => {
      if (client !== ws && client.readyState === ws.OPEN) {
        client.send(JSON.stringify(data));
      }
    });
  });

  ws.on("close", () => console.log("WS client disconnected"));
});

// ---------------- Start Server ----------------
server.listen(PORT, () => {
  console.log(`Express + WS server running on port ${PORT}`);
});
