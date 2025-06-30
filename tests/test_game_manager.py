import io
import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from nash_equilibrium.game_manager import GameManager
from nash_equilibrium.strategic_game import StrategicGame

# Backwards compatibility alias
NormalForm = StrategicGame


def test_game_manager_create_game():
    """Test game creation via GameManager."""
    game_manager = GameManager()

    # Test random game creation
    game_id, game = game_manager.create_game("r", rows=2, columns=2)
    assert game_id == "1"
    assert game.rows == 2
    assert game.columns == 2

    # Test direct payoff matrix creation
    payoff_matrix = [[(3, 3), (0, 5)], [(5, 0), (1, 1)]]
    game_id, game = game_manager.create_game("d", payoff_matrix=payoff_matrix)
    assert game_id == "2"
    assert game.grid == payoff_matrix


def test_game_manager_create_common_game():
    """Test common game creation via GameManager."""
    game_manager = GameManager()

    # Test Prisoner's Dilemma
    game_id, game = game_manager.create_common_game("prisoners_dilemma")
    assert game_id == "1"
    assert game.grid[0][0] == (3, 3)  # Default values
    assert game.grid[1][1] == (1, 1)  # Default values

    # Test Coordination Game
    game_id, game = game_manager.create_common_game("coordination")
    assert game_id == "2"
    assert game.grid[0][0] == (5, 5)  # Default values
    assert game.grid[1][1] == (3, 3)  # Default values

    # Test Battle of Sexes
    game_id, game = game_manager.create_common_game("battle_of_sexes")
    assert game_id == "3"
    assert game.grid[0][0] == (3, 2)  # Default values
    assert game.grid[1][1] == (2, 3)  # Default values

    # Test Zero-Sum Game
    with patch("random.randint", return_value=1):
        game_id, game = game_manager.create_common_game("zero_sum")
        assert game_id == "4"
        assert game.grid[0][0][0] + game.grid[0][0][1] == 0  # Sum should be 0
        assert game.grid[1][1][0] + game.grid[1][1][1] == 0  # Sum should be 0


def test_game_manager_analyze_game():
    """Test game analysis via GameManager."""
    game_manager = GameManager()

    # Create a Prisoner's Dilemma
    game_id, _ = game_manager.create_common_game("prisoners_dilemma")

    # Analyze for Nash equilibria
    analysis = game_manager.analyze_game(game_id)

    assert "pure_nash" in analysis
    assert len(analysis["pure_nash"]) == 1
    assert analysis["pure_nash"][0] == (1, 1)  # Bottom-right is the Nash equilibrium

    # Test non-existent game
    with pytest.raises(KeyError):
        game_manager.analyze_game("nonexistent_id")


def test_game_manager_calculate_expected_payoffs():
    """Test expected payoff calculations."""
    game_manager = GameManager()

    # Create a Prisoner's Dilemma
    game_id, _ = game_manager.create_common_game("prisoners_dilemma")

    # Calculate expected payoffs with specific mixed strategies
    p1_strategy = [0.5, 0.5]  # 50% cooperate, 50% defect
    p2_strategy = [0.5, 0.5]  # 50% cooperate, 50% defect

    eps = game_manager.calculate_expected_payoffs(game_id, p1_strategy, p2_strategy)

    assert len(eps) == 2
    assert isinstance(eps[0], (int, float))
    assert isinstance(eps[1], (int, float))

    # For Prisoner's Dilemma with these mixed strategies:
    # EV for P1 should be (0.5*0.5)*3 + (0.5*0.5)*0 + (0.5*0.5)*5 + (0.5*0.5)*1 = 2.25
    # EV for P2 should be (0.5*0.5)*3 + (0.5*0.5)*5 + (0.5*0.5)*0 + (0.5*0.5)*1 = 2.25
    assert abs(eps[0] - 2.25) < 0.001
    assert abs(eps[1] - 2.25) < 0.001


def test_game_manager_export_game():
    """Test game export functionality."""
    game_manager = GameManager()

    # Create a simple 2x2 game
    payoff_matrix = [[(1, 1), (2, 0)], [(0, 2), (3, 3)]]
    game_id, _ = game_manager.create_game("d", payoff_matrix=payoff_matrix)

    # Export as dict
    game_dict = game_manager.export_game(game_id, format="dict")
    assert isinstance(game_dict, dict)
    assert "payoff_matrix" in game_dict
    assert "rows" in game_dict
    assert "columns" in game_dict

    # Export as JSON
    game_json = game_manager.export_game(game_id, format="json")
    assert isinstance(game_json, str)
    assert '"payoff_matrix"' in game_json
    assert '"rows"' in game_json
    assert '"columns"' in game_json

    # Test invalid format
    with pytest.raises(ValueError):
        game_manager.export_game(game_id, format="invalid")


def test_normal_form_get_payoffs():
    """Test getting payoffs from NormalForm."""
    payoff_matrix = [[(1, 2), (3, 4)], [(5, 6), (7, 8)]]
    game = NormalForm(mode="d", payoff_matrix=payoff_matrix)

    p1_payoffs = game.get_payoffs(player=1)
    p2_payoffs = game.get_payoffs(player=2)

    assert p1_payoffs == [[1, 3], [5, 7]]
    assert p2_payoffs == [[2, 4], [6, 8]]


def test_normal_form_calculate_expected_payoffs():
    """Test the calculate_expected_payoffs method."""
    payoff_matrix = [[(3, 3), (0, 5)], [(5, 0), (1, 1)]]
    game = NormalForm(mode="d", payoff_matrix=payoff_matrix)

    # Test for player 1 with specific beliefs about player 2
    p2_beliefs = [0.7, 0.3]  # Player 2 plays column 1 with 70% probability
    p1_eps = game.calculate_expected_payoffs(player=1, beliefs=p2_beliefs)

    # Expected values:
    # Strategy A1: 0.7*3 + 0.3*0 = 2.1
    # Strategy A2: 0.7*5 + 0.3*1 = 3.8
    assert abs(p1_eps["A1"] - 2.1) < 0.001
    assert abs(p1_eps["A2"] - 3.8) < 0.001

    # Test for player 2 with specific beliefs about player 1
    p1_beliefs = [0.4, 0.6]  # Player 1 plays row 1 with 40% probability
    p2_eps = game.calculate_expected_payoffs(player=2, beliefs=p1_beliefs)

    # Expected values:
    # Strategy B1: 0.4*3 + 0.6*0 = 1.2
    # Strategy B2: 0.4*5 + 0.6*1 = 2.6
    assert abs(p2_eps["B1"] - 1.2) < 0.001
    assert abs(p2_eps["B2"] - 2.6) < 0.001


def test_normal_form_get_formatted_normal_form():
    """Test the formatted output of normal form."""
    payoff_matrix = [[(1, 2), (3, 4)], [(5, 6), (7, 8)]]
    game = NormalForm(mode="d", payoff_matrix=payoff_matrix)

    formatted = game.get_formatted_normal_form()
    assert isinstance(formatted, str)
    assert "A1" in formatted
    assert "A2" in formatted
    assert "B1" in formatted
    assert "B2" in formatted
