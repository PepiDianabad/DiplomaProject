import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, TextField, Typography, Container, Box, Paper, Avatar } from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import axios from 'axios';

const SignIn = ({ setUser }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // state to hold error messages
  const navigate = useNavigate();

  const handleSubmit = async (e) => { // add async keyword here
    e.preventDefault();
    
    if (username && password) {
      try {
        console.log(username, password);
        const response = await axios.post('http://ab7b03b63143d403cbd93c8e5d35c4d3-1864689775.eu-central-1.elb.amazonaws.com:5000/auth/login', {
          username,
          password,
        });

        const userId = response.data.userId; //get the user id from the backend auth
        // Handle successful login, e.g., set user and navigate
        setUser({ username });
        console.log(response.data);
        // after successful login
        navigate('/', { state: { userId } }); // Navigate to the home page after successful login and pass the user id
      } catch (err) {
        setError('Invalid username or password');
      }
    } else {
      alert('Please enter both username and password');
    }
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
      <Container 
        maxWidth="xs" 
        style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center', 
          justifyContent: 'center',
        }}
      >
        <Paper 
          elevation={6} 
          style={{ padding: '30px', borderRadius: '15px', width: '100%', backgroundColor: '#ffffffee' }}
        >
          <Box display="flex" flexDirection="column" alignItems="center" mb={3}>
            <Avatar style={{ backgroundColor: '#3f51b5', marginBottom: '15px' }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography variant="h5" component="h1" style={{ fontWeight: 'bold', color: '#333' }}>
              Sign In
            </Typography>
          </Box>

          <form onSubmit={handleSubmit}>
            <TextField
              label="Username"
              variant="outlined"
              fullWidth
              margin="normal"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoFocus
            />
            <TextField
              label="Password"
              type="password"
              variant="outlined"
              fullWidth
              margin="normal"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button 
              type="submit" 
              variant="contained" 
              color="primary" 
              fullWidth 
              style={{ marginTop: '20px', padding: '10px 0', fontSize: '16px' }}
            >
              Sign In
            </Button>
            {error && <Typography color="error">{error}</Typography>} {/* Display error message */}
          </form>
        </Paper>
      </Container>
    </div>
  );
};

export default SignIn;
