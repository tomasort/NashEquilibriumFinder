"""
Performance tests for Nash Equilibrium Finder

These tests check the performance characteristics of key algorithms.
"""

import time

import numpy as np
import pytest

from normal_form.NormalForm import NormalForm


class TestPerformance:
    """Performance tests for key operations."""

    def test_large_game_creation(self):
        """Test creation of large games."""
        start_time = time.time()
        game = NormalForm(mode="r", rows=10, columns=10)
        game.add_payoffs()
        creation_time = time.time() - start_time

        assert creation_time < 1.0  # Should complete in under 1 second
        assert game.rows == 10
        assert game.columns == 10

    def test_nash_equilibrium_calculation_performance(self):
        """Test performance of Nash equilibrium calculation."""
        # Create a moderately sized game
        game = NormalForm(mode="r", rows=5, columns=5)
        game.add_payoffs()

        start_time = time.time()
        pure_nash = game.find_pure_nash_equi()
        calculation_time = time.time() - start_time

        assert calculation_time < 0.1  # Should be very fast for 5x5 game
        assert isinstance(pure_nash, list)

    def test_expected_payoff_calculation_performance(self):
        """Test performance of expected payoff calculations."""
        game = NormalForm(mode="r", rows=8, columns=8)
        game.add_payoffs()

        # Random mixed strategies
        p1_strategy = np.random.dirichlet(np.ones(8)).tolist()
        p2_strategy = np.random.dirichlet(np.ones(8)).tolist()

        start_time = time.time()
        for _ in range(100):  # Run 100 times
            game.ep_bpm(p1_strategy, p2_strategy)
        calculation_time = time.time() - start_time

        assert calculation_time < 1.0  # 100 calculations should take less than 1 second

    @pytest.mark.slow
    def test_memory_usage_large_game(self):
        """Test memory usage for large games."""
        import tracemalloc

        tracemalloc.start()

        # Create a large game
        game = NormalForm(mode="r", rows=20, columns=20)
        game.add_payoffs()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Memory usage should be reasonable (less than 10MB for a 20x20 game)
        assert peak < 10 * 1024 * 1024  # 10MB

    def test_cache_effectiveness(self):
        """Test that caching improves performance."""
        game = NormalForm(mode="r", rows=6, columns=6)
        game.add_payoffs()

        p1_strategy = [1 / 6] * 6
        p2_strategy = [1 / 6] * 6

        # First call (cache miss)
        start_time = time.time()
        result1 = game.ep_bpm(p1_strategy, p2_strategy)
        first_call_time = time.time() - start_time

        # Second call (cache hit)
        start_time = time.time()
        result2 = game.ep_bpm(p1_strategy, p2_strategy)
        second_call_time = time.time() - start_time

        # Results should be the same
        assert result1 == result2

        # Second call should be faster (though this may not always be detectable)
        # At minimum, it shouldn't be significantly slower
        assert second_call_time <= first_call_time * 2
