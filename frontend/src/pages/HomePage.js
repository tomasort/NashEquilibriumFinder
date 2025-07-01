import React from 'react';
import { 
  Box, 
  Typography,
  Paper,
  Grid,
  Button,
  Card,
  CardContent,
  CardMedia,
  CardActions
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const HomePage = () => {
  // Common game examples
  const gameExamples = [
    {
      title: "Prisoner's Dilemma",
      description: "Classic game theory problem where two prisoners must decide whether to cooperate or defect.",
      image: "https://via.placeholder.com/350x150?text=Prisoner's+Dilemma",
      gameType: "prisoners_dilemma"
    },
    {
      title: "Battle of Sexes",
      description: "Coordination game where two players have different preferences but want to coordinate.",
      image: "https://via.placeholder.com/350x150?text=Battle+of+Sexes",
      gameType: "battle_of_sexes"
    },
    {
      title: "Coordination Game",
      description: "Players must coordinate on the same strategy to maximize their payoffs.",
      image: "https://via.placeholder.com/350x150?text=Coordination+Game",
      gameType: "coordination"
    },
    {
      title: "Zero Sum Game",
      description: "Game where one player's gain is exactly balanced by the other's loss.",
      image: "https://via.placeholder.com/350x150?text=Zero+Sum+Game",
      gameType: "zero_sum"
    }
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Paper 
        elevation={0}
        sx={{ 
          p: 6, 
          mb: 4, 
          bgcolor: 'primary.main', 
          color: 'white',
          borderRadius: 2
        }}
      >
        <Typography variant="h3" component="h1" gutterBottom>
          Nash Equilibrium Finder
        </Typography>
        <Typography variant="h6" sx={{ mb: 4 }}>
          A powerful tool for analyzing 2-player normal form games from game theory
        </Typography>
        <Button 
          variant="contained" 
          color="secondary" 
          size="large"
          component={RouterLink}
          to="/create"
        >
          Create a Game
        </Button>
      </Paper>

      {/* Features Section */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          Features
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Pure & Mixed Nash Equilibria
              </Typography>
              <Typography variant="body2">
                Find both pure and mixed strategy Nash equilibria in strategic games.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Expected Payoffs
              </Typography>
              <Typography variant="body2">
                Calculate expected payoffs for any mixed strategy profile.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Best Responses
              </Typography>
              <Typography variant="body2">
                Find best responses to given strategies or beliefs.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Common Game Templates
              </Typography>
              <Typography variant="body2">
                Create and analyze standard games like Prisoner's Dilemma or Battle of Sexes.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Custom Games
              </Typography>
              <Typography variant="body2">
                Define your own payoff matrices or generate random games.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Visual Analysis
              </Typography>
              <Typography variant="body2">
                Interactive visualizations of game matrices and equilibria.
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>

      {/* Common Games Section */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          Common Game Examples
        </Typography>
        <Grid container spacing={3}>
          {gameExamples.map((game, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="img"
                  height="140"
                  image={game.image}
                  alt={game.title}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h6" component="div">
                    {game.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {game.description}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button size="small" component={RouterLink} to={`/create?template=${game.gameType}`}>
                    Try This Example
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Getting Started Section */}
      <Box>
        <Typography variant="h4" component="h2" gutterBottom>
          Getting Started
        </Typography>
        <Paper sx={{ p: 3 }}>
          <Typography variant="body1" paragraph>
            To get started, create a game using one of the templates or define your own payoff matrix. 
            Once you've created a game, you can analyze it for Nash equilibria, calculate expected payoffs, 
            and test different strategies.
          </Typography>
          <Button 
            variant="contained" 
            color="primary"
            component={RouterLink}
            to="/create"
            sx={{ mr: 2 }}
          >
            Create a Game
          </Button>
          <Button 
            variant="outlined" 
            color="primary"
            component={RouterLink}
            to="/tutorial"
          >
            View Tutorial
          </Button>
        </Paper>
      </Box>
    </Box>
  );
};

export default HomePage;
