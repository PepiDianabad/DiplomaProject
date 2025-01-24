import React, { useState } from 'react';
import { Container, Typography, TextField, Button, Box, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

const Interview = () => {
  const [questions, setQuestions] = useState([]); // state for questions from the backend
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState([]);
  const [showNextQuestionButton, setShowNextQuestionButton] = useState(false);
  const [showResultsButton, setShowResultsButton] = useState(false);
  const [selectedSector, setSelectedSector] = useState('');
  const [selectedDegree, setSelectedDegree] = useState('');
  const [isInterviewStarted, setIsInterviewStarted] = useState(false); // new state for interview status
  const [answers, setAnswers] = useState([]); // state for answers  
  const navigate = useNavigate();
  const location = useLocation();
  const { userId } = location.state || {};

  // sectors and degrees
  const sectors = [
    "Web Developer",
    "Engineer",
    "Teacher",
    "DevOps Specialist",
    "Data Scientist",
    "Product Manager",
    "Graphic Designer",
    "Marketing Specialist",
    "System Administrator",
    "UX/UI Designer",
  ];

  const degrees = [
    "Junior",
    "Mid-Level",
    "Senior",
    "Lead",
    "Expert"
  ];

  const handleNextQuestion = () => {
    if (answer.trim() === '') {
      alert('Please provide an answer.');
      return;
    }

    setAnswers(prevAnswers => [...prevAnswers, answer]); // add answer to answers array

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setAnswer('');
    } else {
      setShowNextQuestionButton(false);
      setShowResultsButton(true);
    }
  };

  const handleStartInterview = async () => {
    if (!selectedSector || !selectedDegree) {
      alert('Please select both a sector and a degree.');
      return;
    }

    const interviewData = {
      type: `${selectedSector} ${selectedDegree}`,
      userId: userId,
    };

    try {
      const response = await axios.post('http://a7314a4ee04f744208c1e93d79a7412e-850590677.eu-central-1.elb.amazonaws.com:5000/interviews/aiquestions', interviewData);
      setQuestions(response.data.questions); // assuming questions are returned as an array
      setShowNextQuestionButton(true);
      setCurrentQuestion(0);
      setIsInterviewStarted(true);
    } catch (error) {
      console.error('Error fetching questions:', error);
      alert('Error fetching questions. Please try again.');
    }
  };

  const handleViewResults = async () => {
    console.log('Starting to view results...');
    
    const interviewData = {
      type: `${selectedSector} ${selectedDegree}`,
      questions: feedback.map((item) => item.question).join(', '),
      feedback: feedback.map((item) => item.feedback).join(', '),
      userId: userId,
    };
  
    const feedbackData = {
      questions: questions, // array
      answers: answers      // array
    };
  
    try {
      console.log('Sending feedback data:', feedbackData);
      
      const feedbackResponse = await axios.post('http://a7314a4ee04f744208c1e93d79a7412e-850590677.eu-central-1.elb.amazonaws.com:5000/interviews/aifeedback', feedbackData);
      
      console.log("Received feedback response:", feedbackResponse.data.feedback);

      interviewData.feedback = feedbackResponse.data.feedback;
  
      await axios.post('http://a7314a4ee04f744208c1e93d79a7412e-850590677.eu-central-1.elb.amazonaws.com:5000/interviews', interviewData);
      console.log("Interview data submittedd");
  
      navigate('/results', { state: { results: feedbackResponse.data, userId: interviewData.userId } });
    } catch (error) {
      console.error('Error submitting interview:', error.response ? error.response.data : error.message);
      alert('Error submitting interview. Please try again.');
    }
  };
  
  return (
    <Container maxWidth="sm" style={{ marginTop: '50px', textAlign: 'center' }}>
      <Typography variant="h4" gutterBottom>
        Interview Question {currentQuestion + 1}/{questions.length || 0}
      </Typography>

      <FormControl fullWidth style={{ marginBottom: '20px' }}>
        <InputLabel id="sector-select-label">Select Sector</InputLabel>
        <Select
          labelId="sector-select-label"
          value={selectedSector}
          onChange={(e) => setSelectedSector(e.target.value)}
          label="Select Sector"
        >
          {sectors.map((sector, index) => (
            <MenuItem key={index} value={sector}>{sector}</MenuItem>
          ))}
        </Select>
      </FormControl>

      <FormControl fullWidth style={{ marginBottom: '20px' }}>
        <InputLabel id="degree-select-label">Select Degree</InputLabel>
        <Select
          labelId="degree-select-label"
          value={selectedDegree}
          onChange={(e) => setSelectedDegree(e.target.value)}
          label="Select Degree"
        >
          {degrees.map((degree, index) => (
            <MenuItem key={index} value={degree}>{degree}</MenuItem>
          ))}
        </Select>
      </FormControl>

      {!isInterviewStarted && (
        <Button
          variant="contained"
          color="primary"
          onClick={handleStartInterview}
          sx={{ marginBottom: '20px', width: '100%', padding: '10px' }}
        >
          Start Interview
        </Button>
      )}

      <Typography variant="h6" gutterBottom>
        {questions[currentQuestion] || "Select a sector and degree to get started!"}
      </Typography>

      <Box sx={{ margin: '20px 0' }}>
        <TextField
          fullWidth
          label="Your Answer"
          multiline
          rows={4}
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          variant="outlined"
        />
      </Box>

      {showNextQuestionButton && (
        <Button
          variant="contained"
          color="primary"
          onClick={handleNextQuestion}
          sx={{ marginBottom: '20px', width: '100%', padding: '10px' }}
        >
          {currentQuestion < questions.length - 1 ? 'Next Question' : 'Finish Interview'}
        </Button>
      )}

      {showResultsButton && (
        <Button
          variant="contained"
          color="secondary"
          onClick={handleViewResults}
          sx={{ marginBottom: '20px', width: '100%', padding: '10px' }}
        >
          View Results
        </Button>
      )}
      
      {selectedDegree && (
        <Typography variant="h6" style={{ marginTop: '20px' }}>
          Selected Degree: {selectedDegree}
        </Typography>
      )}
    </Container>
  );
};

export default Interview;
