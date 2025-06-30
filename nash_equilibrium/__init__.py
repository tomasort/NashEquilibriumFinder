"""
Nash Equilibrium Finder Package

A Python library for analyzing 2-player normal form games and finding Nash equilibria.
"""

__version__ = "1.0.0"
__author__ = "Tomas Ortega and Pablo Mueller"
__email__ = "contact@nashequilibrium.dev"
__license__ = "MIT"

from .parser import GameFileParseError, GameFileParser
from .game_manager import GameManager
from .strategic_game import StrategicGame
from .utils import from_list_to_beliefs, get_coordinates_string

# Backwards compatibility
NormalForm = StrategicGame

__all__ = [
    "StrategicGame",
    "NormalForm",  # Keep for backwards compatibility
    "GameManager",
    "GameFileParser",
    "GameFileParseError",
    "from_list_to_beliefs",
    "get_coordinates_string",
]
