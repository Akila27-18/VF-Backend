// ===============================
// server.js  (Final Corrected)
// ===============================

import express from "express";
import { WebSocketServer } from "ws";
import http from "http";
import cors from "cors";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import pkg from "pg";
import fetch from "node-fetch";
import dotenv from "dotenv";

dotenv.config();

const { Pool } = pkg;

const PORT = process.env.PORT || 8000;
const JWT_SECRET = process.env.JWT_SECRET || "dev-secret";

// ===============================
// PostgreSQL Connection
// ===============================
const pool = new Pool({
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT),
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

// ===============================
// Express
// ===============================
const app = express();
app.use(cors({
  origin: "https://peaceful-gingersnap-de1052.netlify.app",
  credentials: true
}));
app.use(express.json());

// ===============================
// Helper Functions
// ===============================
async function createUser(username, password) {
  const hash = await bcrypt.hash(password, 10);
  const res = await pool.query(
    `INSERT INTO app_user (username, password)
     VALUES ($1, $2)
     RETURNING id, username`,
    [username, hash]
  );
  return res.rows[0];
}

async function authenticateUser(username, password) {
  const res = await pool.query(
    "SELECT * FROM app_user WHERE username=$1",
    [username]
  );

  if (res.rowCount === 0) return null;

  const user = res.rows[0];
  const valid = await bcrypt.compare(password, user.password);
  return valid ? user : null;
}

// ===============================
// Signup
// ===============================
app.post("/api/signup", async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password)
    return res.status(400).json({ error: "Username and password required" });

  try {
    const exists = await pool.query(
      "SELECT 1 FROM app_user WHERE username=$1",
      [username]
    );

    if (exists.rowCount)
      return res.status(400).json({ error: "User already exists" });

    const user = await createUser(username, password);
    const token = jwt.sign(
      { username: user.username, id: user.id },
      JWT_SECRET,
      { expiresIn: "1d" }
    );

    res.json({ token, username: user.username });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal server error" });
  }
});

// ===============================
// Login
// ===============================
app.post("/api/login", async (req, res) => {
  const { username, password } = req.body;

  try {
    const user = await authenticateUser(username, password);
    if (!user) return res.status(401).json({ error: "Invalid credentials" });

    const token = jwt.sign(
      { username: user.username, id: user.id },
      JWT_SECRET,
      { expiresIn: "1d" }
    );

    res.json({ token, username: user.username });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal server error" });
  }
});

// ===============================
// JWT Middleware
// ===============================
const authenticate = (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader)
    return res.status(401).json({ error: "No token provided" });

  const token = authHeader.split(" ")[1];
  try {
    req.user = jwt.verify(token, JWT_SECRET);
    next();
  } catch (err) {
    res.status(401).json({ error: "Invalid token" });
  }
};

// ===============================
// Protected Test Route
// ===============================
app.get("/api/protected", authenticate, (req, res) => {
  res.json({ message: `Hello ${req.user.username}, you are authenticated!` });
});

// ===============================
// Mock Stock API
// ===============================
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

// ===============================
// WebSocket Server
// ===============================
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

wss.on("connection", (ws) => {
  console.log("WS client connected");

  ws.on("message", async (msg) => {
    try {
      const data = JSON.parse(msg);

      if (data.type === "chat") {
        const { from, text } = data.payload;

        await pool.query(
          `INSERT INTO chat_chatmessage (
            from_user, text, time, delivered, seen, created_at
          ) VALUES ($1, $2, $3, false, false, NOW())`,
          [from, text, new Date().toLocaleTimeString()]
        );
      }

      // broadcast
      wss.clients.forEach((client) => {
        if (client.readyState === 1)
          client.send(JSON.stringify(data));
      });

    } catch (err) {
      console.error("Invalid JSON", err);
    }
  });

  ws.on("close", () => console.log("WS client disconnected"));
});

// ===============================
// Auto Stock Updates (every 10 sec)
// ===============================
const symbols = ["AAPL", "TSLA", "MSFT", "BTC-USD", "ETH-USD", "RELIANCE.NS"];

setInterval(async () => {
  for (const sym of symbols) {
    const res = await fetch(`${process.env.SERVER_URL}/api/stock/${sym}`);
    const stock = await res.json();

    wss.clients.forEach((client) => {
      if (client.readyState === 1)
        client.send(JSON.stringify({ type: "stock", payload: stock }));
    });
  }
}, 10000);

// ===============================
// Start Server
// ===============================
server.listen(PORT, () => {
  console.log(`Server + WS running on port ${PORT}`);
});
