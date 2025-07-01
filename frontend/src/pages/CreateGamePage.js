import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Box, 
  Typography,
  Grid,
  Alert,
  Snackbar
} from '@mui/material';
import GameCreator from '../components/Games/GameCreator';
import { useGameContext } from '../context/GameContext';
import { createGame, createCommonGame } from '../services/api';

const CreateGamePage = () => {
  const navigate = useNavigate();
  const { loading, error, createGame: contextCreateGame } = useGameContext();
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('info');
  
  // Handle game creation
  const handleCreateGame = async (mode, payload) => {
    try {
      let gameId;
      
      if (mode === 'template') {
        // Use the common game API
        gameId = await contextCreateGame('template', payload);
      } else if (mode === 'random') {
        // Use the random game API
        gameId = await contextCreateGame('random', payload);
      } else {
        // Use the custom game API (not implemented yet)
        setSnackbarMessage('Custom game creation is not yet implemented');
        setSnackbarSeverity('info');
        setSnackbarOpen(true);
        return;
      }
      
      if (gameId) {
        // Show success message
        setSnackbarMessage('Game created successfully!');
        setSnackbarSeverity('success');
        setSnackbarOpen(true);
        
        // Navigate to the analysis page
        setTimeout(() => {
          navigate(`/analysis/${gameId}`);
        }, 1000);
      }
    } catch (err) {
      setSnackbarMessage(err.message || 'Failed to create game');
      setSnackbarSeverity('error');
      setSnackbarOpen(true);
    }
  };
  
  // Handle snackbar close
  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackbarOpen(false);
  };
  
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Create a New Game
      </Typography>
      
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <GameCreator onSubmit={handleCreateGame} loading={loading} />
        </Grid>
      </Grid>
      
      <Snackbar 
        open={snackbarOpen} 
        autoHideDuration={6000} 
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert 
          onClose={handleSnackbarClose} 
          severity={snackbarSeverity} 
          sx={{ width: '100%' }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default CreateGamePage;
