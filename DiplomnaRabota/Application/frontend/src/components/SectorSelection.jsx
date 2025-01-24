// src/SectorSelection.js

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Typography, Container, Box, Paper } from '@mui/material';

const sectors = [
  'Web Developer',
  'Engineer',
  'Teacher',
  'DevOps Specialist',
  'Data Scientist',
  'Project Manager',
  'Graphic Designer',
  'Product Owner',
  'System Analyst',
  'QA Specialist',
];

const SectorSelection = () => {
  const navigate = useNavigate();

  const handleSectorSelect = (sector) => {
    // Navigate to the interview page with the selected sector
    navigate('/interview', { state: { sector } });
  };

  return (
    <Container maxWidth="xs" style={{ marginTop: '50px' }}>
      <Paper elevation={6} style={{ padding: '30px', borderRadius: '15px', backgroundColor: '#ffffffee' }}>
        <Typography variant="h5" component="h1" style={{ fontWeight: 'bold', color: '#333', marginBottom: '20px' }}>
          Select Your Sector
        </Typography>
        <Box display="flex" flexDirection="column" alignItems="center">
          {sectors.map((sector) => (
            <Button
              key={sector}
              variant="contained"
              color="primary"
              fullWidth
              onClick={() => handleSectorSelect(sector)}
              style={{ marginBottom: '15px' }}
            >
              {sector}
            </Button>
          ))}
        </Box>
      </Paper>
    </Container>
  );
};

export default SectorSelection;
