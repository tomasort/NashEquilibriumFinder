import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Box, 
  Typography,
  Grid,
  Paper,
  Button,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Divider
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import PayoffMatrix from '../components/Games/PayoffMatrix';
import { useGameContext } from '../context/GameContext';

const GameAnalysisPage = () => {
  const { gameId } = useParams();
  const navigate = useNavigate();
  const { getGame, analyzeGame, loading, error } = useGameContext();
  
  const [game, setGame] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  
  // Fetch the game data on component mount
  useEffect(() => {
    const fetchGame = async () => {
      const gameData = await getGame(gameId);
      if (gameData) {
        setGame(gameData);
        // Auto-analyze the game
        const analysisData = await analyzeGame(gameId);
        if (analysisData) {
          setAnalysis(analysisData);
        }
      }
    };
    
    fetchGame();
  }, [gameId, getGame, analyzeGame]);
  
  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };
  
  // Navigate to strategy testing page
  const handleTestStrategies = () => {
    navigate(`/strategy/${gameId}`);
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
      {/* Game title and basic info */}
      <Typography variant="h4" component="h1" gutterBottom>
        Game Analysis: Game #{gameId}
      </Typography>
      
      <Grid container spacing={3}>
        {/* Main content */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Game Matrix
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Player 1 payoffs are shown in <span style={{ color: '#e53935', fontWeight: 'bold' }}>red</span>, 
              Player 2 payoffs are shown in <span style={{ color: '#1e88e5', fontWeight: 'bold' }}>blue</span>.
              Nash equilibria (if any) are highlighted in green.
            </Typography>
            
            <Box sx={{ my: 2 }}>
              <PayoffMatrix 
                payoffMatrix={game.payoff_matrix} 
                pureNash={analysis?.pure_nash || []}
              />
            </Box>
          </Paper>
          
          <Paper sx={{ p: 3 }}>
            <Tabs value={activeTab} onChange={handleTabChange} sx={{ mb: 2 }}>
              <Tab label="Nash Equilibria" />
              <Tab label="Best Responses" />
              <Tab label="Mixed Strategies" />
            </Tabs>
            
            <Box hidden={activeTab !== 0}>
              <Typography variant="h6" gutterBottom>
                Pure Strategy Nash Equilibria
              </Typography>
              
              {analysis?.pure_nash && analysis.pure_nash.length > 0 ? (
                <Box sx={{ mt: 2 }}>
                  {analysis.pure_nash.map((equilibrium, index) => (
                    <Typography key={index} variant="body1" sx={{ mb: 1 }}>
                      {`Equilibrium ${index + 1}: (A${equilibrium[0] + 1}, B${equilibrium[1] + 1})`}
                    </Typography>
                  ))}
                </Box>
              ) : (
                <Alert severity="info" sx={{ mt: 2 }}>
                  No pure strategy Nash equilibria found.
                </Alert>
              )}
              
              <Divider sx={{ my: 3 }} />
              
              <Typography variant="h6" gutterBottom>
                Mixed Strategy Nash Equilibria
              </Typography>
              
              {analysis?.mixed_nash ? (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    Player 1's strategy: [{analysis.mixed_nash.p1_strategy.map(p => p.toFixed(2)).join(', ')}]
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    Player 2's strategy: [{analysis.mixed_nash.p2_strategy.map(p => p.toFixed(2)).join(', ')}]
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    Expected payoffs: [{analysis.mixed_nash.expected_payoffs.map(p => p.toFixed(2)).join(', ')}]
                  </Typography>
                </Box>
              ) : (
                <Alert severity="info" sx={{ mt: 2 }}>
                  Mixed strategy Nash equilibria analysis not available or not applicable.
                </Alert>
              )}
            </Box>
            
            <Box hidden={activeTab !== 1}>
              <Typography variant="h6" gutterBottom>
                Best Responses
              </Typography>
              {/* Best responses content - to be implemented */}
              <Alert severity="info" sx={{ mt: 2 }}>
                Best response analysis is not yet implemented in this UI.
              </Alert>
            </Box>
            
            <Box hidden={activeTab !== 2}>
              <Typography variant="h6" gutterBottom>
                Mixed Strategies
              </Typography>
              <Typography variant="body1" paragraph>
                To experiment with different mixed strategies and calculate expected payoffs, 
                use the Strategy Testing page.
              </Typography>
              <Button 
                variant="contained" 
                color="primary"
                startIcon={<PlayArrowIcon />}
                onClick={handleTestStrategies}
              >
                Test Strategies
              </Button>
            </Box>
          </Paper>
        </Grid>
        
        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Game Details
            </Typography>
            <Typography variant="body1">
              <strong>Dimensions:</strong> {game.rows} × {game.columns}
            </Typography>
            <Typography variant="body1">
              <strong>Player 1 Strategies:</strong> {Array.from({ length: game.rows }, (_, i) => `A${i + 1}`).join(', ')}
            </Typography>
            <Typography variant="body1">
              <strong>Player 2 Strategies:</strong> {Array.from({ length: game.columns }, (_, i) => `B${i + 1}`).join(', ')}
            </Typography>
            
            <Box sx={{ mt: 3 }}>
              <Button 
                variant="outlined" 
                fullWidth
                startIcon={<AnalyticsIcon />}
                onClick={handleTestStrategies}
              >
                Test Strategies
              </Button>
            </Box>
          </Paper>
          
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Game Theory Concepts
            </Typography>
            <Typography variant="body2" paragraph>
              <strong>Nash Equilibrium:</strong> A set of strategies where no player can benefit by changing their strategy while the other players keep theirs unchanged.
            </Typography>
            <Typography variant="body2" paragraph>
              <strong>Pure Strategy:</strong> A player's decision is deterministic, choosing exactly one action.
            </Typography>
            <Typography variant="body2">
              <strong>Mixed Strategy:</strong> A player's decision is probabilistic, assigning probabilities to each possible action.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default GameAnalysisPage;
