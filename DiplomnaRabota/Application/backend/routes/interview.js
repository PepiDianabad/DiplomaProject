const express = require('express');
const router = express.Router();
const Interview = require('../models/InterviewModel'); 
const generateAIQuestions = require('./aiquestions'); // Generate AI questions
const generateAIFeedback = require('./aifeedback'); // Generate AI feedback

// POST /aiquestions route to generate AI questions
router.post('/aiquestions', async (req, res) => {
  const { type } = req.body; 
  const [sector, degree] = type.split(' '); 

  try {
    const aiQuestions = await generateAIQuestions(sector, degree);
    res.status(200).json({ questions: aiQuestions }); 
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to generate AI questions' });
  }
});

// POST / route to create an interview with AI-generated questions
router.post('/', async (req, res) => {
  const { type, feedback, userId } = req.body; 
  const [sector, degree] = type.split(' '); 

  try {
    const aiQuestions = await generateAIQuestions(sector, degree);
    
    const newInterview = await Interview.create({
      type,
      questions: aiQuestions.join(', '), 
      feedback,
      userId,
    });

    res.status(201).json({ newInterview });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to create interview' });
  }
});

// POST /aifeedback route to generate feedback based on interview questions and answers
router.post('/aifeedback', async (req, res) => {
  const feedbackData = req.body;
  console.log(feedbackData);

  try {
    const feedback = await generateAIFeedback(feedbackData); // Placeholder feedback

    res.status(200).json({ feedback }); 
  } catch (error) {
    console.error('Error generating feedback:', error);
    res.status(500).json({ error: 'Failed to generate feedback' });
  }
});

// Export the router
module.exports = router;
