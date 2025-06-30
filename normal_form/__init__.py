"""
Nash Equilibrium Finder Package

A Python library for analyzing 2-player normal form games and finding Nash equilibria.
"""

__version__ = "1.0.0"
__author__ = "Tomas Ortega and Pablo Mueller"
__email__ = "contact@nashequilibrium.dev"
__license__ = "MIT"

from .game_file_parser import GameFileParseError, GameFileParser
from .game_manager import GameManager
from .NormalForm import NormalForm
from .utils import from_list_to_beliefs, get_coordinates_string

__all__ = [
    "NormalForm",
    "GameManager",
    "GameFileParser",
    "GameFileParseError",
    "from_list_to_beliefs",
    "get_coordinates_string",
]
