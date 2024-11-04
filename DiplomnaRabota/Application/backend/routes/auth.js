const express = require('express');
const router = express.Router();
const User = require('../models/UserModel');
const bcrypt = require('bcryptjs'); // bcrypt to hash and compare passwords

// POST /login route to validate username and password
router.post('/login', async (req, res) => {
  const { username, password } = req.body;

  try {
    // find user by username
    const user = await User.findOne({ where: { username } });
    
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // compare the password with hashed password stored in the database
    const isMatch = await bcrypt.compare(password, user.password);

    if (!isMatch) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    res.json({ message: 'Login successful', userId: user.id });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
});

// POST /signup route to create a new user
router.post('/signup', async (req, res) => {
  const { username, password } = req.body;

  try {
    // check if the user already exists - ne dava 2 usera s ednakuv username
    const existingUser = await User.findOne({ where: { username } });
    
    if (existingUser) {
      return res.status(400).json({ error: 'Username already exists' });
    }

    // hash the password
    const hashedPassword = await bcrypt.hash(password, 10);

    // create a new user with the model class
    const newUser = await User.create({
      username, 
      password: hashedPassword, 
    });

    
    res.status(201).json({ message: 'User registered successfully', userId: newUser.id });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
