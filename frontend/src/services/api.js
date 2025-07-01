import axios from 'axios';

// Base URL for API requests
const API_BASE_URL = '/api';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Create a new game
 * 
 * @param {string} mode - 'r' (random) or 'd' (direct)
 * @param {Object} params - Parameters for game creation
 * @returns {Promise} - Promise with game data
 */
export const createGame = async (mode, params) => {
  const payload = { mode, ...params };
  
  try {
    const response = await api.post('/games', payload);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Create a common game type
 * 
 * @param {string} gameType - Type of game ('prisoners_dilemma', 'coordination', etc.)
 * @param {Object} params - Additional parameters specific to the game type
 * @returns {Promise} - Promise with game data
 */
export const createCommonGame = async (gameType, params = {}) => {
  const payload = { game_type: gameType, ...params };
  
  try {
    const response = await api.post('/common-games', payload);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Get a game by ID
 * 
 * @param {string} gameId - ID of the game
 * @returns {Promise} - Promise with game data
 */
export const getGame = async (gameId) => {
  try {
    const response = await api.get(`/games/${gameId}`);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Analyze a game for Nash equilibria
 * 
 * @param {string} gameId - ID of the game
 * @param {Object} options - Analysis options
 * @param {boolean} options.findNash - Whether to find pure Nash equilibria
 * @param {boolean} options.findMixed - Whether to calculate mixed strategy Nash equilibrium
 * @returns {Promise} - Promise with analysis results
 */
export const analyzeGame = async (gameId, options = {}) => {
  const { findNash = true, findMixed = true } = options;
  
  try {
    const response = await api.get(`/games/${gameId}/analyze`, {
      params: {
        find_nash: findNash,
        find_mixed: findMixed
      }
    });
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Calculate expected payoffs with mixed strategies
 * 
 * @param {string} gameId - ID of the game
 * @param {Array} p1Strategy - Player 1's mixed strategy (list of probabilities)
 * @param {Array} p2Strategy - Player 2's mixed strategy (list of probabilities)
 * @returns {Promise} - Promise with expected payoffs
 */
export const calculateExpectedPayoffs = async (gameId, p1Strategy, p2Strategy) => {
  const payload = {
    p1_strategy: p1Strategy,
    p2_strategy: p2Strategy
  };
  
  try {
    const response = await api.post(`/games/${gameId}/expected-payoffs`, payload);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Generate random mixed strategies
 * 
 * @param {string} gameId - ID of the game
 * @param {string} mode - Method for generating random probabilities ('dirichlet' or 'sum')
 * @returns {Promise} - Promise with random beliefs
 */
export const generateRandomBeliefs = async (gameId, mode = 'dirichlet') => {
  try {
    const response = await api.get(`/games/${gameId}/random-beliefs`, {
      params: { mode }
    });
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Handle API errors
 * 
 * @param {Error} error - Axios error object
 * @returns {Error} - Processed error
 */
const handleApiError = (error) => {
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    const serverError = error.response.data.error || 'Server error';
    return new Error(serverError);
  } else if (error.request) {
    // The request was made but no response was received
    return new Error('No response from server. Please check your connection.');
  } else {
    // Something happened in setting up the request that triggered an Error
    return new Error('Error setting up request: ' + error.message);
  }
};
