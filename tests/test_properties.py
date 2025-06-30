"""
Mathematical property tests for Nash Equilibrium Finder

These tests verify mathematical properties of the algorithms using
predefined test cases and parametrized tests.
"""

import numpy as np
import pytest

from nash_equilibrium.strategic_game import StrategicGame

# Backwards compatibility alias
NormalForm = StrategicGame


def create_test_games():
    """Create a variety of test games for property testing."""
    games = []
    
    # 2x2 games
    games.append(NormalForm(mode="d", payoff_matrix=[[(3, 3), (0, 5)], [(5, 0), (1, 1)]]))  # Prisoner's Dilemma
    games.append(NormalForm(mode="d", payoff_matrix=[[(5, 5), (0, 0)], [(0, 0), (3, 3)]]))  # Coordination
    games.append(NormalForm(mode="d", payoff_matrix=[[(3, 2), (0, 0)], [(0, 0), (2, 3)]]))  # Battle of Sexes
    games.append(NormalForm(mode="d", payoff_matrix=[[(1, -1), (-1, 1)], [(-1, 1), (1, -1)]]))  # Zero-sum
    
    # 2x3 games
    games.append(NormalForm(mode="d", payoff_matrix=[[(1, 2), (3, 1), (2, 3)], [(2, 1), (1, 3), (0, 2)]]))
    games.append(NormalForm(mode="d", payoff_matrix=[[(4, 1), (0, 2), (2, 0)], [(1, 3), (3, 1), (1, 4)]]))
    
    # 3x2 games  
    games.append(NormalForm(mode="d", payoff_matrix=[[(2, 3), (1, 1)], [(3, 2), (0, 4)], [(1, 0), (2, 2)]]))
    games.append(NormalForm(mode="d", payoff_matrix=[[(5, 1), (2, 2)], [(1, 3), (4, 1)], [(3, 0), (1, 5)]]))
    
    # 3x3 games
    games.append(NormalForm(mode="d", payoff_matrix=[
        [(1, 1), (2, 0), (0, 2)], 
        [(0, 2), (1, 1), (2, 0)], 
        [(2, 0), (0, 2), (1, 1)]
    ]))
    
    return games


def create_valid_mixed_strategy(size):
    """Generate a valid mixed strategy (probabilities that sum to 1)."""
    # Create random positive numbers and normalize
    np.random.seed(42)  # For reproducibility
    values = np.random.uniform(0.1, 10.0, size)
    total = sum(values)
    return [v / total for v in values]


class TestGameProperties:
    """Test mathematical properties of games."""

    @pytest.mark.parametrize("game", create_test_games())
    def test_game_structure_consistency(self, game):
        """Test that games maintain consistent structure."""
        assert game.rows > 0
        assert game.columns > 0
        assert len(game.grid) == game.rows
        assert all(len(row) == game.columns for row in game.grid)
        assert all(isinstance(cell, tuple) and len(cell) == 2 for row in game.grid for cell in row)

    @pytest.mark.parametrize("game", create_test_games())
    def test_pure_nash_equilibria_properties(self, game):
        """Test properties of pure Nash equilibria."""
        nash_eq = game.find_pure_nash_equi()

        # All equilibria should be valid coordinates
        for eq in nash_eq:
            assert isinstance(eq, tuple)
            assert len(eq) == 2
            assert 0 <= eq[0] < game.columns  # x-coordinate (column) should be within bounds
            assert 0 <= eq[1] < game.rows     # y-coordinate (row) should be within bounds

    @pytest.mark.parametrize("game", create_test_games())
    def test_best_response_properties(self, game):
        """Test properties of best responses."""
        # Test for both players
        for player in [1, 2]:
            br = game.find_br(player)

            # Best responses should be valid coordinates
            for response in br:
                assert isinstance(response, tuple)
                assert len(response) == 2
                assert 0 <= response[0] < game.columns  # x-coordinate (column) should be within bounds
                assert 0 <= response[1] < game.rows     # y-coordinate (row) should be within bounds

    @pytest.mark.parametrize("game", create_test_games())
    def test_expected_payoff_properties(self, game):
        """Test properties of expected payoff calculations."""
        # Generate valid mixed strategies
        p1_strategy = [1.0 / game.rows] * game.rows  # Uniform strategy
        p2_strategy = [1.0 / game.columns] * game.columns

        p1_ep, p2_ep = game.ep_bpm(p1_strategy, p2_strategy)

        # Expected payoffs should be finite numbers
        assert isinstance(p1_ep, (int, float))
        assert isinstance(p2_ep, (int, float))
        assert not np.isnan(p1_ep)
        assert not np.isnan(p2_ep)
        assert not np.isinf(p1_ep)
        assert not np.isinf(p2_ep)

    def test_strategy_validation_properties(self):
        """Test strategy validation with various inputs."""
        # Test with a 2x2 game
        game = NormalForm(mode="d", payoff_matrix=[[(3, 3), (0, 5)], [(5, 0), (1, 1)]])

        # Valid strategies should pass validation
        valid_p1 = create_valid_mixed_strategy(game.rows)
        valid_p2 = create_valid_mixed_strategy(game.columns)

        assert game.validate_strategy(valid_p1, 1)
        assert game.validate_strategy(valid_p2, 2)

        # Invalid strategies should fail
        with pytest.raises(ValueError):
            # Wrong length
            game.validate_strategy([0.5, 0.5, 0.0], 1)  # 3 elements for 2-strategy player

        with pytest.raises(ValueError):
            # Doesn't sum to 1
            invalid_strategy = [0.3, 0.3]  # Sums to 0.6, not 1.0
            game.validate_strategy(invalid_strategy, 1)

        # Test with a 3x3 game
        game_3x3 = NormalForm(mode="d", payoff_matrix=[
            [(1, 1), (2, 0), (0, 2)], 
            [(0, 2), (1, 1), (2, 0)], 
            [(2, 0), (0, 2), (1, 1)]
        ])

        # Valid strategies should pass
        valid_3_strategy = create_valid_mixed_strategy(3)
        assert game_3x3.validate_strategy(valid_3_strategy, 1)
        assert game_3x3.validate_strategy(valid_3_strategy, 2)

    @pytest.mark.parametrize("game", create_test_games())
    def test_symmetry_properties(self, game):
        """Test symmetry properties where applicable."""
        # If it's a symmetric game, certain properties should hold
        if game.rows == game.columns:
            # Check if the game is symmetric
            is_symmetric = True
            for i in range(game.rows):
                for j in range(game.columns):
                    if game.grid[i][j][0] != game.grid[j][i][1] or game.grid[i][j][1] != game.grid[j][i][0]:
                        is_symmetric = False
                        break
                if not is_symmetric:
                    break

            if is_symmetric:
                # In symmetric games, if (i,j) is a Nash equilibrium,
                # then (j,i) might also be one (depending on the specific game)
                nash_eq = game.find_pure_nash_equi()
                # This is a weak property - just check that we can find equilibria
                assert isinstance(nash_eq, list)


class TestNumericalProperties:
    """Test numerical stability and edge cases."""

    @pytest.mark.parametrize("p", [0.1, 0.3, 0.5, 0.7, 0.9])
    def test_strategy_normalization(self, p):
        """Test that strategies are properly normalized."""
        # Create a simple 2x2 game
        game = NormalForm(mode="d", payoff_matrix=[[(1, 1), (0, 0)], [(0, 0), (1, 1)]])

        # Create a strategy that needs normalization
        strategy = [p, 1 - p]

        # Should be valid
        assert game.validate_strategy(strategy, 1)

        # Expected payoff should work
        p1_ep, p2_ep = game.ep_bpm(strategy, [0.5, 0.5])
        assert not np.isnan(p1_ep)
        assert not np.isnan(p2_ep)

    def test_edge_case_zero_payoffs(self):
        """Test games with zero payoffs."""
        # All zero payoffs
        game = NormalForm(mode="d", payoff_matrix=[[(0, 0), (0, 0)], [(0, 0), (0, 0)]])

        # Should still work
        nash_eq = game.find_pure_nash_equi()
        assert isinstance(nash_eq, list)

        # All strategies should be Nash equilibria
        assert len(nash_eq) == 4  # All four outcomes

    def test_edge_case_identical_payoffs(self):
        """Test games where all payoffs are identical."""
        # All same payoffs
        game = NormalForm(mode="d", payoff_matrix=[[(5, 3), (5, 3)], [(5, 3), (5, 3)]])

        nash_eq = game.find_pure_nash_equi()
        assert isinstance(nash_eq, list)
        # All outcomes should be Nash equilibria since no player can improve
        assert len(nash_eq) == 4
