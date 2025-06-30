"""
Type definitions for Nash Equilibrium Finder

This module contains type hints and aliases used throughout the project.
"""

from typing import Any, Dict, List, Tuple, Union

# Basic types
Payoff = Union[int, float]
PayoffPair = Tuple[Payoff, Payoff]
PayoffMatrix = List[List[PayoffPair]]
Strategy = List[float]  # Mixed strategy (probabilities)
Coordinates = Tuple[int, int]  # (row, col) coordinates

# Game analysis results
NashEquilibria = List[Coordinates]
BestResponses = List[Coordinates]
ExpectedPayoffs = Tuple[float, float]  # (player1_payoff, player2_payoff)

# Mixed strategy results
MixedStrategyResult = Dict[str, Union[Strategy, str, None]]
AnalysisResult = Dict[str, Any]

# File parsing
GameData = Dict[str, Any]
ParseResult = Tuple[str, Any]  # (game_id, game_object)
