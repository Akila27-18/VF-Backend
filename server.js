import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { WebSocketServer } from "ws";
import sequelize from "./config/db.js"; // Sequelize instance
import Expense from "./models/Expense.js";
import User from "./models/User.js";
import Message from "./models/Message.js";
import expensesRoutes from "./routes/expenses.js";
import authRoutes from "./routes/auth.js";

dotenv.config();
const app = express();
app.use(cors());
app.use(express.json());

// -------------------------------
// AUTH + EXPENSES ROUTES
// -------------------------------
app.use("/auth", authRoutes);
app.use("/expenses", expensesRoutes);

// -------------------------------
// MOCK STOCK ENDPOINT
// -------------------------------
app.get("/api/stock/:symbol", (req, res) => {
  const symbol = req.params.symbol;
  const price = +(Math.random() * 500 + 100).toFixed(2);
  const change = +(Math.random() * 10 - 5).toFixed(2);

  res.json({
    symbol,
    price,
    change,
    percent: +((change / price) * 100).toFixed(2),
    spark: Array.from({ length: 20 }, () =>
      +(price + Math.random() * 5 - 2).toFixed(2)
    ),
  });
});

// -------------------------------
// MYSQL / SEQUELIZE CONNECTION
// -------------------------------
async function connectDB() {
  try {
    await sequelize.authenticate();
    console.log("MySQL connected via Sequelize");

    // Sync models
    await User.sync();
    await Expense.sync();
    await Message.sync();
    console.log("Models synced");
  } catch (err) {
    console.error("Sequelize connection error:", err);
    process.exit(1);
  }
}
connectDB();

// -------------------------------
// START HTTP SERVER
// -------------------------------
const PORT = process.env.PORT || 5000;
const server = app.listen(PORT, () =>
  console.log(`API running on port ${PORT}`)
);

// -------------------------------
// WEBSOCKET SERVER
// -------------------------------
const wss = new WebSocketServer({ server, path: "/ws/chat" });
console.log("WebSocket server running at ws://localhost:" + PORT + "/ws/chat");

wss.on("connection", async (ws) => {
  console.log("WS client connected");

  // Send last 50 messages to new client
  try {
    const lastMessages = await Message.findAll({
      order: [["createdAt", "ASC"]],
      limit: 50,
    });
    lastMessages.forEach((msg) => {
      ws.send(JSON.stringify({ type: "chat", payload: msg }));
    });
  } catch (err) {
    console.error("Failed to load messages:", err);
  }

  // Handle incoming messages
  ws.on("message", async (message) => {
    let data;
    try { data = JSON.parse(message); } 
    catch (error) { console.error("Invalid JSON:", error); return; }

    // Save chat message to DB
    if (data.type === "chat" && data.payload?.id) {
      try {
        await Message.create({
          id: data.payload.id,
          from: data.payload.from,
          text: data.payload.text,
          time: data.payload.time,
        });
      } catch (err) {
        console.error("Failed to save message:", err);
      }
    }

    // Broadcast to all clients
    wss.clients.forEach((client) => {
      if (client.readyState === 1) client.send(JSON.stringify(data));
    });
  });

  ws.on("close", () => console.log("WS client disconnected"));
});

// -------------------------------
// AUTO STOCK BROADCAST
// -------------------------------
const symbols = ["AAPL", "TSLA", "MSFT", "BTC-USD", "ETH-USD", "RELIANCE.NS"];
setInterval(() => {
  symbols.forEach((sym) => {
    const price = +(Math.random() * 500 + 100).toFixed(2);
    const change = +(Math.random() * 10 - 5).toFixed(2);
    const stockUpdate = {
      type: "stock",
      payload: {
        symbol: sym,
        price,
        change,
        percent: +((change / price) * 100).toFixed(2),
        spark: Array.from({ length: 20 }, () => +(price + Math.random() * 5 - 2).toFixed(2)),
      },
    };
    wss.clients.forEach((client) => {
      if (client.readyState === 1) client.send(JSON.stringify(stockUpdate));
    });
  });
}, 10000);

// -------------------------------
// MOCK NEWS ENDPOINT
// -------------------------------
app.get("/api/news", (req, res) => {
  const news = [
    { headline: "Market rallies as tech stocks surge", url: "https://example.com/article1", datetime: Date.now() / 1000 },
    { headline: "Global economy shows signs of recovery", url: "https://example.com/article2", datetime: Date.now() / 1000 - 3600 },
    { headline: "Investors eye new opportunities in AI sector", url: "https://example.com/article3", datetime: Date.now() / 1000 - 7200 },
    { headline: "Cryptocurrency volatility shakes markets", url: "https://example.com/article4", datetime: Date.now() / 1000 - 10800 },
  ];
  res.json(news);
});

// -------------------------------
// MESSAGES PAGINATION ENDPOINT
// -------------------------------
import { Op } from "sequelize";
app.get("/api/messages", async (req, res) => {
  const before = req.query.before ? new Date(req.query.before) : new Date();
  const limit = parseInt(req.query.limit) || 20;

  try {
    const messages = await Message.findAll({
      where: { createdAt: { [Op.lt]: before } },
      order: [["createdAt", "DESC"]],
      limit,
    });
    res.json(messages.reverse());
  } catch (err) {
    console.error("Failed to fetch messages:", err);
    res.status(500).json({ error: "Failed to fetch messages" });
  }
});
