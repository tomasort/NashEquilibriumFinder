import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Slider,
  Alert,
  CircularProgress,
  Button,
  Divider,
  Card,
  CardContent
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import { useGameContext } from '../context/GameContext';
import PayoffMatrix from '../components/Games/PayoffMatrix';

const StrategyTestingPage = () => {
  const { gameId } = useParams();
  const navigate = useNavigate();
  const { getGame, calculateExpectedPayoffs, loading, error } = useGameContext();

  const [game, setGame] = useState(null);
  const [p1Strategy, setP1Strategy] = useState([]);
  const [p2Strategy, setP2Strategy] = useState([]);
  const [expectedPayoffs, setExpectedPayoffs] = useState(null);
  const [calculating, setCalculating] = useState(false);

  // Fetch the game data on component mount
  useEffect(() => {
    const fetchGame = async () => {
      const gameData = await getGame(gameId);
      if (gameData) {
        setGame(gameData);
        // Initialize strategies with uniform distributions
        const p1InitialStrategy = Array(gameData.rows).fill(1 / gameData.rows);
        const p2InitialStrategy = Array(gameData.columns).fill(1 / gameData.columns);
        setP1Strategy(p1InitialStrategy);
        setP2Strategy(p2InitialStrategy);
      }
    };

    fetchGame();
  }, [gameId, getGame]);

  // Calculate expected payoffs when strategies change
  const handleCalculate = async () => {
    setCalculating(true);
    try {
      const payoffs = await calculateExpectedPayoffs(gameId, p1Strategy, p2Strategy);
      if (payoffs) {
        setExpectedPayoffs(payoffs);
      }
    } catch (err) {
      console.error("Error calculating payoffs:", err);
    } finally {
      setCalculating(false);
    }
  };

  // Update strategy with new probabilities, ensuring they sum to 1
  const updateStrategy = (player, index, newValue) => {
    if (player === 1) {
      const newStrategy = [...p1Strategy];
      newStrategy[index] = newValue / 100;
      
      // Calculate the sum of all other probabilities
      const otherSum = newStrategy.reduce((acc, curr, i) => i !== index ? acc + curr : acc, 0);
      
      // If the sum of other probabilities is 0, set all other probabilities to equal values
      if (otherSum === 0) {
        const remainingProb = (1 - newStrategy[index]) / (newStrategy.length - 1);
        newStrategy.forEach((_, i) => {
          if (i !== index) newStrategy[i] = remainingProb;
        });
      } else {
        // Scale other probabilities to make the sum equal 1
        const scale = (1 - newStrategy[index]) / otherSum;
        newStrategy.forEach((prob, i) => {
          if (i !== index) newStrategy[i] = prob * scale;
        });
      }
      
      setP1Strategy(newStrategy);
    } else {
      const newStrategy = [...p2Strategy];
      newStrategy[index] = newValue / 100;
      
      // Calculate the sum of all other probabilities
      const otherSum = newStrategy.reduce((acc, curr, i) => i !== index ? acc + curr : acc, 0);
      
      // If the sum of other probabilities is 0, set all other probabilities to equal values
      if (otherSum === 0) {
        const remainingProb = (1 - newStrategy[index]) / (newStrategy.length - 1);
        newStrategy.forEach((_, i) => {
          if (i !== index) newStrategy[i] = remainingProb;
        });
      } else {
        // Scale other probabilities to make the sum equal 1
        const scale = (1 - newStrategy[index]) / otherSum;
        newStrategy.forEach((prob, i) => {
          if (i !== index) newStrategy[i] = prob * scale;
        });
      }
      
      setP2Strategy(newStrategy);
    }
  };

  // Loading state
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  // Error state
  if (error) {
    return (
      <Box sx={{ maxWidth: 600, mx: 'auto', p: 2 }}>
        <Alert severity="error">
          {error}
        </Alert>
      </Box>
    );
  }

  // Game not found state
  if (!game) {
    return (
      <Box sx={{ maxWidth: 600, mx: 'auto', p: 2 }}>
        <Alert severity="warning">
          Game not found or failed to load. Please try again.
        </Alert>
        <Button
          variant="contained"
          sx={{ mt: 2 }}
          onClick={() => navigate('/create')}
        >
          Create a New Game
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Strategy Testing: Game #{gameId}
      </Typography>

      <Grid container spacing={3}>
        {/* Main content */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Game Matrix
            </Typography>
            <Box sx={{ my: 2 }}>
              <PayoffMatrix
                payoffMatrix={game.payoff_matrix}
              />
            </Box>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Mixed Strategy Testing
            </Typography>
            <Typography variant="body2" paragraph>
              Adjust the sliders to set the probabilities for each strategy. The probabilities will automatically be normalized to sum to 1.
            </Typography>

            <Box sx={{ mt: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Player 1's Strategy
              </Typography>
              {p1Strategy.map((prob, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={2}>
                      <Typography variant="body2">A{index + 1}</Typography>
                    </Grid>
                    <Grid item xs={8}>
                      <Slider
                        value={Math.round(prob * 100)}
                        onChange={(e, value) => updateStrategy(1, index, value)}
                        aria-labelledby={`p1-strategy-${index}`}
                        valueLabelDisplay="auto"
                        valueLabelFormat={value => `${value}%`}
                      />
                    </Grid>
                    <Grid item xs={2}>
                      <Typography variant="body2" textAlign="right">
                        {(prob * 100).toFixed(0)}%
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
              ))}
            </Box>

            <Divider sx={{ my: 3 }} />

            <Box sx={{ mt: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Player 2's Strategy
              </Typography>
              {p2Strategy.map((prob, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={2}>
                      <Typography variant="body2">B{index + 1}</Typography>
                    </Grid>
                    <Grid item xs={8}>
                      <Slider
                        value={Math.round(prob * 100)}
                        onChange={(e, value) => updateStrategy(2, index, value)}
                        aria-labelledby={`p2-strategy-${index}`}
                        valueLabelDisplay="auto"
                        valueLabelFormat={value => `${value}%`}
                      />
                    </Grid>
                    <Grid item xs={2}>
                      <Typography variant="body2" textAlign="right">
                        {(prob * 100).toFixed(0)}%
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
              ))}
            </Box>

            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Button
                variant="contained"
                color="primary"
                size="large"
                startIcon={<PlayArrowIcon />}
                onClick={handleCalculate}
                disabled={calculating}
              >
                {calculating ? 'Calculating...' : 'Calculate Expected Payoffs'}
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Expected Payoffs
              </Typography>
              {expectedPayoffs ? (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    <strong>Player 1:</strong> {expectedPayoffs[0].toFixed(3)}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Player 2:</strong> {expectedPayoffs[1].toFixed(3)}
                  </Typography>
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  Click "Calculate Expected Payoffs" to see the results
                </Typography>
              )}
            </CardContent>
          </Card>

          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Current Strategy Profile
            </Typography>
            <Typography variant="body2" paragraph>
              <strong>Player 1:</strong> [{p1Strategy.map(p => p.toFixed(2)).join(', ')}]
            </Typography>
            <Typography variant="body2">
              <strong>Player 2:</strong> [{p2Strategy.map(p => p.toFixed(2)).join(', ')}]
            </Typography>

            <Box sx={{ mt: 3 }}>
              <Button
                variant="outlined"
                fullWidth
                onClick={() => navigate(`/analysis/${gameId}`)}
              >
                Back to Analysis
              </Button>
            </Box>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              About Mixed Strategies
            </Typography>
            <Typography variant="body2" paragraph>
              A mixed strategy is a probability distribution over pure strategies. It allows players to randomize their choices.
            </Typography>
            <Typography variant="body2">
              Expected payoffs represent the average outcome when players use mixed strategies. Nash equilibrium in mixed strategies occurs when neither player can improve their expected payoff by unilaterally changing their strategy.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StrategyTestingPage;
