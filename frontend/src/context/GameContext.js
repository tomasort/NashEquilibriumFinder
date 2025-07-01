import React, { createContext, useState, useContext } from 'react';
import { createGame, createCommonGame, getGame, analyzeGame, calculateExpectedPayoffs } from '../services/api';

// Create context
const GameContext = createContext();

// Provider component
export const GameProvider = ({ children }) => {
  const [games, setGames] = useState({});
  const [currentGameId, setCurrentGameId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Create a new game
  const handleCreateGame = async (mode, params) => {
    setLoading(true);
    setError(null);
    
    try {
      let result;
      if (mode === 'template') {
        result = await createCommonGame(params.gameType, params.params);
      } else {
        result = await createGame(params.mode, params);
      }
      
      setGames(prevGames => ({
        ...prevGames,
        [result.game_id]: result.game
      }));
      setCurrentGameId(result.game_id);
      setLoading(false);
      return result.game_id;
    } catch (err) {
      setError(err.message || 'Failed to create game');
      setLoading(false);
      return null;
    }
  };

  // Get a game by ID
  const handleGetGame = async (gameId) => {
    if (games[gameId]) {
      setCurrentGameId(gameId);
      return games[gameId];
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const game = await getGame(gameId);
      setGames(prevGames => ({
        ...prevGames,
        [gameId]: game
      }));
      setCurrentGameId(gameId);
      setLoading(false);
      return game;
    } catch (err) {
      setError(err.message || 'Failed to get game');
      setLoading(false);
      return null;
    }
  };

  // Analyze a game
  const handleAnalyzeGame = async (gameId, options = {}) => {
    setLoading(true);
    setError(null);
    
    try {
      const analysis = await analyzeGame(gameId, options);
      setLoading(false);
      return analysis;
    } catch (err) {
      setError(err.message || 'Failed to analyze game');
      setLoading(false);
      return null;
    }
  };

  // Calculate expected payoffs
  const handleCalculateExpectedPayoffs = async (gameId, p1Strategy, p2Strategy) => {
    setLoading(true);
    setError(null);
    
    try {
      const payoffs = await calculateExpectedPayoffs(gameId, p1Strategy, p2Strategy);
      setLoading(false);
      return payoffs.expected_payoffs;
    } catch (err) {
      setError(err.message || 'Failed to calculate expected payoffs');
      setLoading(false);
      return null;
    }
  };

  // Clear current game
  const clearCurrentGame = () => {
    setCurrentGameId(null);
  };

  // Clear error
  const clearError = () => {
    setError(null);
  };

  // Context value
  const value = {
    games,
    currentGameId,
    currentGame: currentGameId ? games[currentGameId] : null,
    loading,
    error,
    createGame: handleCreateGame,
    getGame: handleGetGame,
    analyzeGame: handleAnalyzeGame,
    calculateExpectedPayoffs: handleCalculateExpectedPayoffs,
    clearCurrentGame,
    clearError
  };

  return <GameContext.Provider value={value}>{children}</GameContext.Provider>;
};

// Custom hook to use the game context
export const useGameContext = () => {
  const context = useContext(GameContext);
  if (!context) {
    throw new Error('useGameContext must be used within a GameProvider');
  }
  return context;
};

export default GameContext;
