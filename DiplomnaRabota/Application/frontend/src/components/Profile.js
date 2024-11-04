import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import { useLocation } from 'react-router-dom';

const Profile = ({ user }) => {
  // sample previous interviews data
  const previousInterviews = [
    { id: 1, date: '2024-09-30', feedback: 'Great answers, but work on your presentation.' },
    { id: 2, date: '2024-10-05', feedback: 'Good technical knowledge, but need to clarify your thought process.' },
  ];

  return (
    <Container maxWidth="sm" style={{ marginTop: '50px', textAlign: 'center' }}>
      <Typography variant="h4" gutterBottom>
        Welcome, {user.username}!
      </Typography>
      <Typography variant="h6" gutterBottom>
        Your Previous Interviews:
      </Typography>

      {previousInterviews.length > 0 ? (
        previousInterviews.map(interview => (
          <Box key={interview.id} sx={{ margin: '20px 0', padding: '10px', border: '1px solid #ccc', borderRadius: '5px' }}>
            <Typography variant="body1">Date: {interview.date}</Typography>
            <Typography variant="body1">Feedback: {interview.feedback}</Typography>
          </Box>
        ))
      ) : (
        <Typography variant="body1">No previous interviews found.</Typography>
      )}
    </Container>
  );
};

export default Profile;
