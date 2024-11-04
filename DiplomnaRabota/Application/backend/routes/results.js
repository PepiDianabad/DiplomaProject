const express = require('express');
const router = express.Router();
const Interview = require('../models/InterviewModel');

// GET /interviews/:userId route to fetch interviews for a specific user
router.get('/:userId', async (req, res) => {
  const { userId } = req.params;

  try {
    const interviews = await Interview.findAll({ where: { userId } }); // Adjusted to match your model's userId field
    res.json(interviews);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
