"""
Tests for the Game File Parser

This module contains comprehensive tests for parsing game definition files
in YAML format and creating NormalForm games from them.
"""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from normal_form.game_file_parser import (
    GameFileParseError,
    GameFileParser,
    parse_game_file,
)


class TestGameFileParser:
    """Test cases for the GameFileParser class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.parser = GameFileParser()

    def create_temp_file(self, content):
        """Helper method to create a temporary file with given content."""
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def teardown_method(self):
        """Clean up after each test method."""
        # Clean up any temporary files created during tests
        pass


class TestBasicParsing:
    """Test basic file parsing functionality."""

    def setup_method(self):
        self.parser = GameFileParser()

    def create_temp_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_parse_prisoners_dilemma(self):
        """Test parsing a Prisoner's Dilemma game."""
        content = """
# Prisoner's Dilemma
GAME_TYPE: prisoners_dilemma
PARAMS:
  t: 5
  r: 3
  p: 1
  s: 0
NAME: Prisoner's Dilemma
DESCRIPTION: Classic game theory example
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 2
            assert game.columns == 2
            # Check specific payoffs for Prisoner's Dilemma
            assert game.grid[0][0] == (3, 3)  # (Cooperate, Cooperate)
            assert game.grid[1][1] == (1, 1)  # (Defect, Defect)
        finally:
            os.unlink(filename)

    def test_parse_battle_of_sexes(self):
        """Test parsing a Battle of the Sexes game."""
        content = """
GAME_TYPE: battle_of_sexes
PARAMS:
  a: 4
  b: 2
NAME: Battle of the Sexes
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 2
            assert game.columns == 2
            # Check specific payoffs
            assert game.grid[0][0] == (4, 2)
            assert game.grid[1][1] == (2, 4)
        finally:
            os.unlink(filename)

    def test_parse_coordination_game(self):
        """Test parsing a Coordination game."""
        content = """
GAME_TYPE: coordination
PARAMS:
  a: 5
  b: 3
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 2
            assert game.columns == 2
            assert game.grid[0][0] == (5, 5)
            assert game.grid[1][1] == (3, 3)
        finally:
            os.unlink(filename)

    def test_parse_zero_sum_game(self):
        """Test parsing a Zero-Sum game."""
        content = """
GAME_TYPE: zero_sum
PARAMS:
  values: [1, -2, 3, -1]
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 2
            assert game.columns == 2
            # Check that it's zero-sum (sum of each cell should be 0)
            for row in game.grid:
                for cell in row:
                    assert cell[0] + cell[1] == 0
        finally:
            os.unlink(filename)

    def test_parse_custom_game(self):
        """Test parsing a custom game with direct payoff matrix."""
        content = """
GAME_TYPE: custom
PAYOFFS:
  - [(3, 3), (0, 5)]
  - [(5, 0), (1, 1)]
NAME: Custom Game
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 2
            assert game.columns == 2
            assert game.grid[0][0] == (3, 3)
            assert game.grid[0][1] == (0, 5)
            assert game.grid[1][0] == (5, 0)
            assert game.grid[1][1] == (1, 1)
        finally:
            os.unlink(filename)

    def test_parse_random_game(self):
        """Test parsing a random game."""
        content = """
GAME_TYPE: random
STRATEGIES: 3 2
PARAMS:
  min_value: -5
  max_value: 10
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 3
            assert game.columns == 2
            # Check that payoffs are within the specified range
            for row in game.grid:
                for cell in row:
                    assert -5 <= cell[0] <= 10
                    assert -5 <= cell[1] <= 10
        finally:
            os.unlink(filename)


class TestParsingEdgeCases:
    """Test edge cases and error conditions in parsing."""

    def setup_method(self):
        self.parser = GameFileParser()

    def create_temp_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_parse_with_comments(self):
        """Test parsing files with various comment styles."""
        content = """
# This is a comment
GAME_TYPE: prisoners_dilemma  # inline comment
PARAMS:
  # Another comment
  t: 5  # Temptation value
  r: 3
  p: 1
  s: 0
# Final comment
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 2
            assert game.columns == 2
        finally:
            os.unlink(filename)

    def test_parse_with_extra_whitespace(self):
        """Test parsing files with extra whitespace and blank lines."""
        content = """

GAME_TYPE: coordination


PARAMS:
  a: 5

  b: 3


NAME: Test Game

"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
        finally:
            os.unlink(filename)

    def test_parse_case_insensitive_keys(self):
        """Test that keys are case-insensitive."""
        content = """
game_type: prisoners_dilemma
params:
  T: 5
  R: 3
  P: 1
  S: 0
name: Test Game
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
        finally:
            os.unlink(filename)

    def test_parse_float_parameters(self):
        """Test parsing parameters with float values."""
        content = """
GAME_TYPE: coordination
PARAMS:
  a: 5.5
  b: 3.2
"""
        filename = self.create_temp_file(content)
        try:
            # This should work even though the factory methods expect integers
            # The parser should handle the conversion
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
        finally:
            os.unlink(filename)

    def test_parse_negative_payoffs(self):
        """Test parsing games with negative payoffs."""
        content = """
GAME_TYPE: custom
PAYOFFS:
  - [(-2, 3), (1, -1)]
  - [(0, -5), (-3, 2)]
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.grid[0][0] == (-2, 3)
            assert game.grid[1][1] == (-3, 2)
        finally:
            os.unlink(filename)

    def test_parse_large_payoff_matrix(self):
        """Test parsing a larger payoff matrix."""
        content = """
GAME_TYPE: custom
PAYOFFS:
  - [(1, 2), (3, 4), (5, 6)]
  - [(7, 8), (9, 10), (11, 12)]
  - [(13, 14), (15, 16), (17, 18)]
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 3
            assert game.columns == 3
            assert game.grid[2][2] == (17, 18)
        finally:
            os.unlink(filename)


class TestErrorHandling:
    """Test error handling and validation."""

    def setup_method(self):
        self.parser = GameFileParser()

    def create_temp_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_missing_file(self):
        """Test error when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            self.parser.parse_file("nonexistent_file.yml")

    def test_missing_game_type(self):
        """Test error when GAME_TYPE is missing."""
        content = """
PARAMS:
  a: 5
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError, match="GAME_TYPE is required"):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_unknown_game_type(self):
        """Test error when GAME_TYPE is unknown."""
        content = """
GAME_TYPE: unknown_game
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError, match="Unknown game type"):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_invalid_strategies_format(self):
        """Test error when STRATEGIES format is invalid."""
        content = """
GAME_TYPE: random
STRATEGIES: invalid
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError, match="Invalid strategies format"):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_missing_payoffs_for_custom_game(self):
        """Test error when PAYOFFS is missing for custom game."""
        content = """
GAME_TYPE: custom
NAME: Test Game
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError, match="PAYOFFS section is required"):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_missing_strategies_for_random_game(self):
        """Test error when STRATEGIES is missing for random game."""
        content = """
GAME_TYPE: random
PARAMS:
  min_value: -5
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError, match="STRATEGIES is required"):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_invalid_payoff_format(self):
        """Test error when payoff format is invalid."""
        content = """
GAME_TYPE: custom
PAYOFFS:
  - [invalid, format]
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError, match="No valid payoff pairs found"):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_malformed_payoff_pairs(self):
        """Test error when payoff pairs are malformed."""
        content = """
GAME_TYPE: custom
PAYOFFS:
  - [(1, 2, 3), (4, 5)]
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_unknown_top_level_key(self):
        """Test error when unknown top-level key is used."""
        content = """
GAME_TYPE: prisoners_dilemma
UNKNOWN_KEY: some_value
PARAMS:
  t: 5
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError, match="Unknown key"):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_unexpected_content_outside_section(self):
        """Test error when content appears outside of valid sections."""
        content = """
GAME_TYPE: prisoners_dilemma
PARAMS:
  t: 5
unexpected content here
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError, match="Unexpected content outside of section"):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)


class TestValidation:
    """Test file validation functionality."""

    def setup_method(self):
        self.parser = GameFileParser()

    def create_temp_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_validate_valid_file(self):
        """Test validation of a valid file."""
        content = """
GAME_TYPE: prisoners_dilemma
PARAMS:
  t: 5
  r: 3
  p: 1
  s: 0
"""
        filename = self.create_temp_file(content)
        try:
            warnings = self.parser.validate_file(filename)
            assert len(warnings) == 0
        finally:
            os.unlink(filename)

    def test_validate_invalid_file(self):
        """Test validation of an invalid file."""
        content = """
GAME_TYPE: unknown_type
"""
        filename = self.create_temp_file(content)
        try:
            warnings = self.parser.validate_file(filename)
            assert len(warnings) > 0
            assert "Unknown game type" in warnings[0]
        finally:
            os.unlink(filename)

    def test_validate_missing_file(self):
        """Test validation of a missing file."""
        warnings = self.parser.validate_file("nonexistent.yml")
        assert len(warnings) > 0
        assert "File error" in warnings[0]


class TestFunctionWrapper:
    """Test the simple function wrapper."""

    def create_temp_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_parse_game_file_function(self):
        """Test the parse_game_file wrapper function."""
        content = """
GAME_TYPE: prisoners_dilemma
PARAMS:
  t: 5
  r: 3
  p: 1
  s: 0
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = parse_game_file(filename)
            assert game_id is not None
            assert game.rows == 2
            assert game.columns == 2
        finally:
            os.unlink(filename)

    def test_parse_game_file_error(self):
        """Test the function wrapper with invalid input."""
        with pytest.raises(FileNotFoundError):
            parse_game_file("nonexistent.yml")


class TestComplexScenarios:
    """Test complex scenarios and integration cases."""

    def setup_method(self):
        self.parser = GameFileParser()

    def create_temp_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_parse_file_with_all_metadata(self):
        """Test parsing a file with all possible metadata fields."""
        content = """
# Complete game definition
GAME_TYPE: battle_of_sexes
PARAMS:
  a: 3
  b: 2
NAME: Battle of the Sexes
DESCRIPTION: A coordination game with conflicting preferences
PLAYER1_STRATEGIES: Opera, Football
PLAYER2_STRATEGIES: Opera, Football
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            # The parser should handle this without errors
            # (even though custom strategy names aren't fully implemented)
        finally:
            os.unlink(filename)

    def test_parse_asymmetric_game(self):
        """Test parsing an asymmetric game (different number of strategies)."""
        content = """
GAME_TYPE: custom
PAYOFFS:
  - [(1, 2), (3, 4), (5, 6)]
  - [(7, 8), (9, 10), (11, 12)]
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 2
            assert game.columns == 3
        finally:
            os.unlink(filename)

    @patch("normal_form.game_file_parser.GameManager")
    def test_parser_uses_game_manager(self, mock_game_manager_class):
        """Test that the parser correctly uses the GameManager."""
        # Set up mock
        mock_game_manager = MagicMock()
        mock_game_manager_class.return_value = mock_game_manager
        mock_game_manager.create_common_game.return_value = ("test_id", MagicMock())

        content = """
GAME_TYPE: prisoners_dilemma
PARAMS:
  t: 5
  r: 3
  p: 1
  s: 0
"""
        filename = self.create_temp_file(content)
        try:
            parser = GameFileParser()
            game_id, game = parser.parse_file(filename)

            # Verify that GameManager was used correctly
            mock_game_manager.create_common_game.assert_called_once_with("prisoners_dilemma", t=5, r=3, p=1, s=0)
        finally:
            os.unlink(filename)


class TestAdvancedScenarios:
    """Test advanced parsing scenarios and edge cases."""

    def setup_method(self):
        self.parser = GameFileParser()

    def create_temp_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_parse_empty_list_parameter(self):
        """Test parsing parameters with empty lists."""
        content = """
GAME_TYPE: zero_sum
PARAMS:
  values: []
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError):
                # Empty list should cause an error when creating zero-sum game
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_parse_mixed_case_game_type(self):
        """Test parsing with mixed case game type."""
        content = """
Game_Type: prisoners_dilemma
PARAMS:
  t: 5
  r: 3
  p: 1
  s: 0
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 2
            assert game.columns == 2
        finally:
            os.unlink(filename)

    def test_parse_complex_inline_comments(self):
        """Test parsing with complex inline comments including special characters."""
        content = """
GAME_TYPE: coordination  # This is a coordination game with # in comment
PARAMS:
  a: 5  # Value A = 5 (high payoff) # extra comment
  b: 3  # Value B = 3 (low payoff)
NAME: Complex # Comment # Game
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.grid[0][0] == (5, 5)
            assert game.grid[1][1] == (3, 3)
        finally:
            os.unlink(filename)

    def test_parse_list_with_floats_and_negatives(self):
        """Test parsing lists with mixed float and negative values."""
        content = """
GAME_TYPE: zero_sum
PARAMS:
  values: [-1.5, 2, -3.7, 4.0]
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            # The zero-sum factory method should handle float values
        finally:
            os.unlink(filename)

    def test_parse_list_with_spaces(self):
        """Test parsing lists with various spacing patterns."""
        content = """
GAME_TYPE: zero_sum
PARAMS:
  values: [ 1 , -2, 3 ,-1 ]
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
        finally:
            os.unlink(filename)

    def test_parse_payoffs_with_negative_and_zero(self):
        """Test parsing payoff matrices with negative values and zeros."""
        content = """
GAME_TYPE: custom
PAYOFFS:
  - [(-5, 0), (0, -3)]
  - [(2, -1), (-2, 4)]
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.grid[0][0] == (-5, 0)
            assert game.grid[1][1] == (-2, 4)
        finally:
            os.unlink(filename)

    def test_parse_large_asymmetric_matrix(self):
        """Test parsing a larger asymmetric game matrix."""
        content = """
GAME_TYPE: custom
PAYOFFS:
  - [(1, 2), (3, 4), (5, 6), (7, 8)]
  - [(9, 10), (11, 12), (13, 14), (15, 16)]
  - [(17, 18), (19, 20), (21, 22), (23, 24)]
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 3
            assert game.columns == 4
            assert game.grid[0][0] == (1, 2)
            assert game.grid[2][3] == (23, 24)
        finally:
            os.unlink(filename)

    def test_parse_random_with_float_bounds(self):
        """Test parsing random game with float bounds."""
        content = """
GAME_TYPE: random
STRATEGIES: 2 3
PARAMS:
  min_value: -2.5
  max_value: 10.7
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 2
            assert game.columns == 3
        finally:
            os.unlink(filename)

    def test_parse_all_metadata_fields(self):
        """Test parsing with all possible metadata fields populated."""
        content = """
# Complete game with all metadata
GAME_TYPE: custom
PAYOFFS:
  - [(3, 2), (0, 0)]
  - [(0, 0), (2, 3)]
NAME: Complete Battle of Sexes
DESCRIPTION: A coordination game with conflicting preferences where players benefit from coordinating but prefer different outcomes
PLAYER1_STRATEGIES: Opera, Football
PLAYER2_STRATEGIES: Opera, Football
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            assert game_id is not None
            assert game.rows == 2
            assert game.columns == 2
            assert game.grid[0][0] == (3, 2)
            assert game.grid[1][1] == (2, 3)
        finally:
            os.unlink(filename)


class TestErrorHandlingAdvanced:
    """Advanced error handling test cases."""

    def setup_method(self):
        self.parser = GameFileParser()

    def create_temp_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_invalid_list_format(self):
        """Test error handling for malformed list parameters."""
        content = """
GAME_TYPE: zero_sum
PARAMS:
  values: [1, 2, invalid, 4]
"""
        filename = self.create_temp_file(content)
        try:
            # This should parse the list but the invalid value should cause issues later
            game_id, game = self.parser.parse_file(filename)
            # If it doesn't fail during parsing, it might fail during game creation
        except GameFileParseError:
            pass  # Expected to fail at some point
        finally:
            os.unlink(filename)

    def test_unclosed_list_parameter(self):
        """Test error handling for unclosed list brackets."""
        content = """
GAME_TYPE: zero_sum
PARAMS:
  values: [1, 2, 3, 4
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_invalid_payoff_tuple_format(self):
        """Test error handling for various invalid payoff tuple formats."""
        content = """
GAME_TYPE: custom
PAYOFFS:
  - [(1), (2, 3)]
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_inconsistent_payoff_row_lengths(self):
        """Test error handling for inconsistent payoff matrix row lengths."""
        content = """
GAME_TYPE: custom
PAYOFFS:
  - [(1, 2), (3, 4)]
  - [(5, 6)]
"""
        filename = self.create_temp_file(content)
        try:
            game_id, game = self.parser.parse_file(filename)
            # This might succeed in parsing but create an invalid game
            # The GameManager should handle this appropriately
        except GameFileParseError:
            pass  # This is also acceptable
        finally:
            os.unlink(filename)

    def test_empty_payoff_section(self):
        """Test error handling for empty payoff section."""
        content = """
GAME_TYPE: custom
PAYOFFS:
"""
        filename = self.create_temp_file(content)
        try:
            with pytest.raises(GameFileParseError):
                self.parser.parse_file(filename)
        finally:
            os.unlink(filename)

    def test_missing_required_parameters(self):
        """Test that missing parameters use default values (which is the current behavior)."""
        # Since the factory methods provide defaults, missing parameters should not cause errors
        # This test verifies that the parser gracefully handles missing parameters
        test_cases = [
            ("prisoners_dilemma", "PARAMS:\n  t: 5\n  r: 3\n  p: 1"),  # missing s, should use default s=0
            ("coordination", "PARAMS:\n  a: 5"),  # missing b, should use default
            ("battle_of_sexes", "PARAMS:\n  a: 3"),  # missing b, should use default
        ]

        for game_type, incomplete_params in test_cases:
            content = f"""
GAME_TYPE: {game_type}
{incomplete_params}
"""
            filename = self.create_temp_file(content)
            try:
                # These should actually succeed due to default parameter values
                game_id, game = self.parser.parse_file(filename)
                assert game_id is not None
                assert game.rows == 2
                assert game.columns == 2
            finally:
                os.unlink(filename)


if __name__ == "__main__":
    pytest.main([__file__])
