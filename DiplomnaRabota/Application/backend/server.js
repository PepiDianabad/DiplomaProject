const express = require('express');
const sequelize = require('./config/db'); // Database configuration
const cors = require('cors');

const User = require('./models/UserModel');  
const Interview = require('./models/InterviewModel');

// Routes
const authRoutes = require('./routes/auth');  
const interviewRoutes = require('./routes/interview'); 
const resultsRoutes = require('./routes/results');
const aiQuestionsRoutes = require('./routes/aiquestions');
const aiFeedbackRoutes = require('./routes/aifeedback');

const app = express();
app.use(express.json()); // Parse JSON bodies

// CORS to allow requests from your React app
app.use(cors({
  origin: 'http://a1627368ee5474211ab70d00f923574e-621459643.eu-central-1.elb.amazonaws.com:3001',
  credentials: true 
}));

// test route
app.get('/', (req, res) => {
  res.send('API is running');
});

// use routes
app.use('/auth', authRoutes);
app.use('/interviews', interviewRoutes);
app.use('/results', resultsRoutes);
app.use('/aiquestions', aiQuestionsRoutes);
app.use('/aifeedback', aiFeedbackRoutes);

// Sync the models and start of the server
sequelize.sync()
  .then(() => {
    console.log('Database synced successfully.');
    app.listen(5000, () => {
      console.log('Server running on port 5000');
    });
  })
  .catch((err) => {
    console.error('Error syncing database:', err);
  });
