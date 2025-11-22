import express from "express";
import Expense from "../models/Expense.js";
import auth from "../middleware/auth.js";

const router = express.Router();

// GET all expenses for user
router.get("/", auth, async (req, res) => {
  try {
    const expenses = await Expense.findAll({
      where: { userId: req.user.id },
      order: [
        ["order", "DESC"],
        ["createdAt", "DESC"]
      ],
    });
    res.json(expenses);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

// CREATE
router.post("/", auth, async (req, res) => {
  try {
    const payload = { ...req.body, userId: req.user.id };
    const created = await Expense.create(payload);
    res.json(created);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

// UPDATE
router.put("/:id", auth, async (req, res) => {
  try {
    const [updatedRows, [updatedExpense]] = await Expense.update(req.body, {
      where: { id: req.params.id, userId: req.user.id },
      returning: true,
    });

    if (updatedRows === 0) return res.status(404).json({ error: "Not found" });

    res.json(updatedExpense);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

// DELETE
router.delete("/:id", auth, async (req, res) => {
  try {
    const deletedRows = await Expense.destroy({
      where: { id: req.params.id, userId: req.user.id },
    });

    if (deletedRows === 0) return res.status(404).json({ error: "Not found" });

    res.json({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

export default router;
