const express = require('express');
const sequelize = require('./config/db'); // Database configuration
const cors = require('cors');

// Import models
const User = require('./models/UserModel');  
const Interview = require('./models/InterviewModel');

// Import routes
const authRoutes = require('./routes/auth');  
const interviewRoutes = require('./routes/interview'); 
const resultsRoutes = require('./routes/results');
const aiQuestionsRoutes = require('./routes/aiquestions');
const aiFeedbackRoutes = require('./routes/aifeedback');

const app = express();
app.use(express.json()); // Parse JSON bodies

// Use CORS to allow requests from your React app
app.use(cors({
  origin: 'http://a96e3f3be3757486583750bf450c5d75-357478491.eu-central-1.elb.amazonaws.com:3001', // React app URL
  credentials: true // If you want to allow cookies, authentication headers, etc.
}));

// Test route
app.get('/', (req, res) => {
  res.send('API is running');
});

// Use routes
app.use('/auth', authRoutes);
app.use('/interviews', interviewRoutes);
app.use('/results', resultsRoutes);
app.use('/aiquestions', aiQuestionsRoutes);
app.use('/aifeedback', aiFeedbackRoutes);

// Sync the models and start the server
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
