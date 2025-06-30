"""
Game Manager Module

This module provides a service layer between user interfaces
(CLI or Web) and the core NormalForm class.
"""

import json

from normal_form.NormalForm import (
    NormalForm,
    create_battle_of_sexes,
    create_coordination_game,
    create_prisoners_dilemma,
    create_zero_sum_game,
)


class GameManager:
    """Manages game creation, analysis, and serialization."""

    def __init__(self):
        """Initialize the GameManager."""
        self.games = {}
        self.next_game_id = 1

    def create_game(self, mode, rows=None, columns=None, payoff_matrix=None, lower_limit=-99, upper_limit=99):
        """Create a new game.

        Arguments:
            mode: 'r' for random, 'm' for manual, 'd' for direct payoff matrix
            rows: Number of rows (required for 'r' and 'm')
            columns: Number of columns (required for 'r' and 'm')
            payoff_matrix: Payoff matrix (required for 'd')
            lower_limit: Lower limit for random payoffs
            upper_limit: Upper limit for random payoffs

        Returns:
            Tuple of (game_id, game)
        """
        game = NormalForm(
            mode=mode,
            rows=rows,
            columns=columns,
            payoff_matrix=payoff_matrix,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
        )

        game_id = str(self.next_game_id)
        self.games[game_id] = game
        self.next_game_id += 1

        return game_id, game

    def create_common_game(self, game_type, **kwargs):
        """Create a common game type.

        Arguments:
            game_type: Type of game ('prisoners_dilemma', 'coordination',
                       'battle_of_sexes', 'zero_sum')
            **kwargs: Game - specific parameters

        Returns:
            Tuple of (game_id, game)
        """
        if game_type == "prisoners_dilemma":
            game = create_prisoners_dilemma(**kwargs)
        elif game_type == "coordination":
            game = create_coordination_game(**kwargs)
        elif game_type == "battle_of_sexes":
            game = create_battle_of_sexes(**kwargs)
        elif game_type == "zero_sum":
            game = create_zero_sum_game(**kwargs)
        else:
            raise ValueError(f"Unknown game type: {game_type}")

        game_id = str(self.next_game_id)
        self.games[game_id] = game
        self.next_game_id += 1

        return game_id, game

    def get_game(self, game_id):
        """Get a game by ID.

        Arguments:
            game_id: ID of the game

        Returns:
            NormalForm game object

        Raises:
            KeyError: If game_id is not found
        """
        if game_id not in self.games:
            raise KeyError(f"Game with ID {game_id} not found")

        return self.games[game_id]

    def analyze_game(self, game_id, find_nash=True, find_mixed=True):
        """Analyze a game for Nash equilibria.

        Arguments:
            game_id: ID of the game
            find_nash: Whether to find pure Nash equilibria
            find_mixed: Whether to calculate mixed strategy Nash equilibrium

        Returns:
            Dictionary with analysis results

        Raises:
            KeyError: If game_id is not found
        """
        game = self.get_game(game_id)

        result = {}

        if find_nash:
            # Find pure Nash equilibria
            nash_eq = game.find_pure_nash_equi()
            result["pure_nash"] = nash_eq

        if find_mixed and game.rows == 2 and game.columns == 2:
            # Calculate mixed strategy Nash equilibrium
            mixed_eq = game.get_indifference_probabilities()
            if isinstance(mixed_eq, list):
                result["mixed_nash"] = {
                    "p1_strategy": mixed_eq[0] if mixed_eq else None,
                    "p2_strategy": mixed_eq[1] if mixed_eq else None,
                    "error": None,
                }
            else:
                result["mixed_nash"] = mixed_eq

        return result

    def calculate_expected_payoffs(self, game_id, p1_strategy, p2_strategy):
        """Calculate expected payoffs with mixed strategies.

        Arguments:
            game_id: ID of the game
            p1_strategy: Player 1's mixed strategy (list of probabilities)
            p2_strategy: Player 2's mixed strategy (list of probabilities)

        Returns:
            Tuple of (p1_payoff, p2_payoff)

        Raises:
            KeyError: If game_id is not found
            ValueError: If strategy vectors don't match game dimensions
        """
        game = self.get_game(game_id)

        return game.ep_bpm(p1_strategy, p2_strategy)

    def generate_random_beliefs(self, game_id, mode="dirichlet"):
        """Generate random mixed strategies.

        Arguments:
            game_id: ID of the game
            mode: Method for generating random probabilities ('dirichlet' or 'sum')

        Returns:
            List of [p1_beliefs, p2_beliefs]

        Raises:
            KeyError: If game_id is not found
        """
        game = self.get_game(game_id)

        return game.create_random_beliefs(mode)

    def export_game(self, game_id, format="json"):
        """Export a game to a specific format.

        Arguments:
            game_id: ID of the game
            format: Export format ('json', 'dict')

        Returns:
            Game in requested format

        Raises:
            KeyError: If game_id is not found
            ValueError: If format is not supported
        """
        game = self.get_game(game_id)
        game_dict = game.to_dict()

        if format == "json":
            # Convert NumPy values to Python native types for JSON serialization
            def convert_numpy(obj):
                if isinstance(obj, (list, tuple)):
                    return [convert_numpy(item) for item in obj]
                if isinstance(obj, dict):
                    return {k: convert_numpy(v) for k, v in obj.items()}
                if hasattr(obj, "tolist"):  # NumPy arrays, float64, etc.
                    return obj.tolist()
                return obj

            game_dict = convert_numpy(game_dict)
            return json.dumps(game_dict)
        elif format == "dict":
            return game_dict
        else:
            raise ValueError(f"Unsupported export format: {format}")
