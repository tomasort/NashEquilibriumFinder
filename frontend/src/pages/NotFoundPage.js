import React from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const NotFoundPage = () => {
  return (
    <Box 
      sx={{ 
        display: 'flex', 
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh',
        textAlign: 'center',
        p: 4
      }}
    >
      <Paper 
        elevation={3}
        sx={{ 
          py: 6,
          px: 4,
          maxWidth: 500,
          width: '100%'
        }}
      >
        <Typography variant="h3" component="h1" sx={{ mb: 2 }}>
          404
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          Page Not Found
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Sorry, the page you are looking for doesn't exist or has been moved.
        </Typography>
        <Button 
          variant="contained" 
          component={RouterLink} 
          to="/"
          size="large"
          sx={{ mt: 2 }}
        >
          Back to Home
        </Button>
      </Paper>
    </Box>
  );
};

export default NotFoundPage;
