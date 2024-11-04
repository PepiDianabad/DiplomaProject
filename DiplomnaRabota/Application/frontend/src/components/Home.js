import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import { Button, Typography, Container, Box, Paper } from '@mui/material';

const Home = ({ user }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { userId } = location.state || {}; // access userId from the state

  console.log("home", userId);

  const handleNewInterview = () => {
    navigate('/interview', { state: { userId } });
  };

  const handlePreviousInterviews = () => {
    navigate('/results', {state: {userId} });
  };

  const handleSignIn = () => {
    navigate('/signin');
  };

  const handleSignUp = () => {
    navigate('/signup'); // Navigate to the signup page
  };

  return (
    <div 
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
      }}
    >
      <Container maxWidth="xs">
        <Paper 
          elevation={6} 
          style={{ padding: '30px', borderRadius: '15px', width: '100%', backgroundColor: '#ffffffee' }}
        >
          <Box display="flex" flexDirection="column" alignItems="center" mb={3}>
            <Typography variant="h5" component="h1" style={{ fontWeight: 'bold', color: '#333', marginBottom: '20px' }}>
              Welcome, {user ? user.username : 'Guest'}
            </Typography>

            {user ? (
              <>
                <Button 
                  variant="contained" 
                  color="primary" 
                  fullWidth 
                  onClick={handleNewInterview} 
                  style={{ marginBottom: '15px', padding: '10px 0' }}
                >
                  Start New Interview
                </Button>
                <Button 
                  variant="outlined" 
                  color="primary" 
                  fullWidth 
                  onClick={handlePreviousInterviews}
                  style={{ padding: '10px 0' }}
                >
                  View Previous Interviews
                </Button>
              </>
            ) : (
              <>
                <Typography style={{ color: '#555', marginBottom: '20px' }}>
                  Please sign in to start or view previous interviews.
                </Typography>
                <Button 
                  variant="contained" 
                  color="primary" 
                  fullWidth 
                  onClick={handleSignIn}
                  style={{ padding: '10px 0', marginBottom: '10px' }} 
                >
                  Sign In
                </Button>
                <Button 
                  variant="outlined" 
                  color="primary" 
                  fullWidth 
                  onClick={handleSignUp}
                  style={{ padding: '10px 0' }}
                >
                  Sign Up
                </Button>
              </>
            )}
          </Box>
        </Paper>
      </Container>
    </div>
  );
};

export default Home;
