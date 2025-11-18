import express from "express";
import fetch from "node-fetch";
import { WebSocketServer } from "ws";

const app = express();
const PORT = 8000;
const WS_PORT = 5000;

app.use(express.json());

// Example REST endpoint for stock fetching
app.get("/api/stock/:symbol", async (req, res) => {
  const symbol = req.params.symbol;
  // Replace with real API logic or local mock
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

app.listen(PORT, () => console.log(`REST API running on port ${PORT}`));

// WebSocket server for chat + stocks
const wss = new WebSocketServer({ port: WS_PORT });
console.log(`WebSocket server running on ws://localhost:${WS_PORT}`);

wss.on("connection", (ws) => {
  console.log("Client connected");

  ws.on("message", (msg) => {
    const data = JSON.parse(msg);

    // Broadcast to all other clients
    wss.clients.forEach((client) => {
      if (client.readyState === 1) client.send(JSON.stringify(data));
    });
  });

  ws.on("close", () => console.log("Client disconnected"));
});

// Periodically broadcast stock updates
const symbols = ["AAPL","TSLA","MSFT","BTC-USD","ETH-USD","RELIANCE.NS"];
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
