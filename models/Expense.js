// models/Expense.js
import { DataTypes } from "sequelize";
import sequelize from "../config/db.js"; // Sequelize instance
import User from "./User.js"; // Assuming you have a User model

const Expense = sequelize.define("Expense", {
  id: {
    type: DataTypes.INTEGER.UNSIGNED,
    autoIncrement: true,
    primaryKey: true,
  },
  userId: {
    type: DataTypes.INTEGER.UNSIGNED,
    allowNull: false,
    references: {
      model: User,
      key: "id",
    },
  },
  title: {
    type: DataTypes.STRING,
    defaultValue: "",
  },
  description: {
    type: DataTypes.STRING,
    defaultValue: "",
  },
  amount: {
    type: DataTypes.FLOAT,
    defaultValue: 0,
  },
  category: {
    type: DataTypes.STRING,
    defaultValue: "Other",
  },
  date: {
    type: DataTypes.DATEONLY,
    defaultValue: DataTypes.NOW,
  },
  shared: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
  },
  participants: {
    type: DataTypes.JSON, // store array as JSON
    defaultValue: [],
  },
  paidBy: {
    type: DataTypes.STRING,
    defaultValue: "",
  },
  order: {
    type: DataTypes.BIGINT,
    defaultValue: () => Date.now(),
  },
}, {
  timestamps: true,
});

export default Expense;
