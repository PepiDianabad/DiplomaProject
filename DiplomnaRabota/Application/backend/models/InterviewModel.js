const { Model, DataTypes } = require('sequelize');
const sequelize = require('../config/db');
const User = require('./UserModel'); // Importing User Model


class Interview extends Model {}

Interview.init({
  type: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  questions: {
    type: DataTypes.TEXT,
    allowNull: false,
  },
  feedback: {
    type: DataTypes.TEXT,
    allowNull: true,
  },
  userId: {
    type: DataTypes.INTEGER,
    references: {
      model: 'Users', // user tble is named 'users'
      key: 'id',
    },
    allowNull: false,
  },
}, {
  sequelize,
  modelName: 'Interview',
});

// Define the relation back to User - UserId in the Interview table refers to the ID in the User table
Interview.belongsTo(User, {
  foreignKey: 'userId', // This should match the userId in the User model
  onDelete: 'CASCADE', // Optional: specify what happens when a user is deleted
});

module.exports = Interview;
