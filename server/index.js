import express from "express";
import fetch from "node-fetch";
import { WebSocketServer } from "ws";
import cors from "cors";
import http from "http";

const PORT = process.env.PORT || 8000;
const app = express();

app.use(cors());
app.use(express.json());

// ===== HTTP + WebSocket Share Same Server (Render requirement) =====
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

// ===== REST API for stock =====
app.get("/api/stock/:symbol", async (req, res) => {
  const symbol = req.params.symbol;

  const mockPrice = Math.random() * 500 + 100;
  const mockChange = Math.random() * 10 - 5;

  res.json({
    symbol,
    price: mockPrice,
    change: mockChange,
    percent: ((mockChange / mockPrice) * 100).toFixed(2),
    spark: Array.from({ length: 20 }, () => mockPrice + Math.random() * 5 - 2),
  });
});

// ===== WebSocket logic =====
wss.on("connection", (ws) => {
  console.log("WS client connected");

  ws.on("message", (msg) => {
    const data = JSON.parse(msg);

    // Broadcast to all
    wss.clients.forEach((client) => {
      if (client.readyState === 1) {
        client.send(JSON.stringify(data));
      }
    });
  });

  ws.on("close", () => console.log("WS client disconnected"));
});

// ===== Periodic Stock Push =====
const symbols = ["AAPL", "TSLA", "MSFT", "BTC-USD", "ETH-USD", "RELIANCE.NS"];

setInterval(async () => {
  for (const sym of symbols) {
    const res = await fetch(`http://localhost:${PORT}/api/stock/${sym}`);
    const stock = await res.json();

    wss.clients.forEach((client) => {
      if (client.readyState === 1) {
        client.send(JSON.stringify({ type: "stock", payload: stock }));
      }
    });
  }
}, 10000);

// ===== Start Server =====
server.listen(PORT, () => {
  console.log(`Server + WS running on port ${PORT}`);
});
