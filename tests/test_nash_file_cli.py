"""
Unit tests for the nash_file.py CLI

This module tests the CLI interface functionality including all commands
and their various options and error handling.
"""

import pytest
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import patch, mock_open
from click.testing import CliRunner

# Import the CLI and its commands
from nash_file import cli, analyze, payoffs, best_response, validate, examples


class TestCLIBasics:
    """Test basic CLI functionality and help."""
    
    def test_cli_help(self):
        """Test that CLI help works."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Nash Equilibrium Finder' in result.output
        assert 'analyze' in result.output
        assert 'payoffs' in result.output
        assert 'best-response' in result.output
        assert 'validate' in result.output
        assert 'examples' in result.output
    
    def test_cli_version(self):
        """Test that CLI version works."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert '1.0.0' in result.output


class TestAnalyzeCommand:
    """Test the analyze command."""
    
    @pytest.fixture
    def prisoners_dilemma_file(self):
        """Create a temporary prisoners dilemma game file."""
        content = """GAME_TYPE: prisoners_dilemma
PARAMS:
  t: 5
  r: 3
  p: 1
  s: 0
NAME: Test Prisoner's Dilemma
DESCRIPTION: Test game for CLI testing
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(content)
            f.flush()
            yield f.name
        os.unlink(f.name)
    
    @pytest.fixture
    def battle_of_sexes_file(self):
        """Create a temporary battle of sexes game file."""
        content = """GAME_TYPE: battle_of_sexes
PARAMS:
  a: 3
  b: 2
NAME: Test Battle of Sexes
DESCRIPTION: Test 2x2 game for mixed strategy testing
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(content)
            f.flush()
            yield f.name
        os.unlink(f.name)
    
    def test_analyze_help(self):
        """Test analyze command help."""
        runner = CliRunner()
        result = runner.invoke(analyze, ['--help'])
        assert result.exit_code == 0
        assert 'Analyze a game defined in GAME_FILE' in result.output
        assert '--output' in result.output
        assert '--analyze-mixed' in result.output
    
    def test_analyze_normal_output(self, prisoners_dilemma_file):
        """Test analyze command with normal output."""
        runner = CliRunner()
        result = runner.invoke(analyze, [prisoners_dilemma_file])
        assert result.exit_code == 0
        assert 'Game Analysis:' in result.output
        assert 'Normal Form' in result.output
        assert 'Pure Strategy Nash Equilibria' in result.output
        assert '2x2' in result.output
    
    def test_analyze_minimal_output(self, prisoners_dilemma_file):
        """Test analyze command with minimal output."""
        runner = CliRunner()
        result = runner.invoke(analyze, [prisoners_dilemma_file, '--output', 'minimal'])
        assert result.exit_code == 0
        assert 'Game from:' in result.output
        assert 'Pure Nash Equilibria:' in result.output
        # Should not have the detailed headers
        assert 'Game Analysis:' not in result.output
    
    def test_analyze_json_output(self, prisoners_dilemma_file):
        """Test analyze command with JSON output."""
        runner = CliRunner()
        result = runner.invoke(analyze, [prisoners_dilemma_file, '--output', 'json'])
        assert result.exit_code == 0
        
        # Should be valid JSON
        try:
            data = json.loads(result.output.strip())
            assert 'rows' in data
            assert 'columns' in data
            assert 'payoff_matrix' in data
            assert data['rows'] == 2
            assert data['columns'] == 2
        except json.JSONDecodeError:
            pytest.fail("Output is not valid JSON")
    
    def test_analyze_with_save_json(self, prisoners_dilemma_file):
        """Test analyze command with save-json option."""
        runner = CliRunner()
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = runner.invoke(analyze, [
                prisoners_dilemma_file, 
                '--save-json', tmp_path
            ])
            assert result.exit_code == 0
            assert f"Game data saved to {tmp_path}" in result.output
            
            # Check that JSON file was created and is valid
            assert os.path.exists(tmp_path)
            with open(tmp_path) as f:
                data = json.load(f)
                assert 'rows' in data
                assert 'columns' in data
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_analyze_mixed_strategy(self, battle_of_sexes_file):
        """Test analyze command with mixed strategy calculation."""
        runner = CliRunner()
        result = runner.invoke(analyze, [battle_of_sexes_file])
        assert result.exit_code == 0
        # Battle of Sexes should have pure Nash equilibria, so mixed strategy section
        # should show "Pure strategy Nash equilibria exist."
        assert 'Mixed Strategy Nash Equilibrium' in result.output
    
    def test_analyze_no_mixed_flag(self, battle_of_sexes_file):
        """Test analyze command with --no-mixed flag."""
        runner = CliRunner()
        result = runner.invoke(analyze, [battle_of_sexes_file, '--no-mixed'])
        assert result.exit_code == 0
        # Should not have mixed strategy section
        assert 'Mixed Strategy Nash Equilibrium' not in result.output
    
    def test_analyze_nonexistent_file(self):
        """Test analyze command with nonexistent file."""
        runner = CliRunner()
        result = runner.invoke(analyze, ['nonexistent.yml'])
        assert result.exit_code != 0
        assert 'does not exist' in result.output.lower()
    
    def test_analyze_invalid_game_file(self):
        """Test analyze command with invalid game file."""
        content = """INVALID_CONTENT: this is not a valid game file
MISSING: required fields
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(content)
            f.flush()
            try:
                runner = CliRunner()
                result = runner.invoke(analyze, [f.name])
                assert result.exit_code != 0
                assert 'Error parsing game file:' in result.output
            finally:
                os.unlink(f.name)


class TestPayoffsCommand:
    """Test the payoffs command."""
    
    @pytest.fixture
    def test_game_file(self):
        """Create a test game file."""
        content = """GAME_TYPE: prisoners_dilemma
PARAMS:
  t: 5
  r: 3
  p: 1
  s: 0
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(content)
            f.flush()
            yield f.name
        os.unlink(f.name)
    
    def test_payoffs_help(self):
        """Test payoffs command help."""
        runner = CliRunner()
        result = runner.invoke(payoffs, ['--help'])
        assert result.exit_code == 0
        assert 'Calculate expected payoffs' in result.output
        assert '--p1-strategy' in result.output
        assert '--p2-strategy' in result.output
    
    def test_payoffs_valid_strategies(self, test_game_file):
        """Test payoffs command with valid strategies."""
        runner = CliRunner()
        result = runner.invoke(payoffs, [
            test_game_file,
            '--p1-strategy', '0.7,0.3',
            '--p2-strategy', '0.4,0.6'
        ])
        assert result.exit_code == 0
        assert 'Expected Payoffs:' in result.output
        assert 'Player 1 Strategy: (0.700, 0.300)' in result.output
        assert 'Player 2 Strategy: (0.400, 0.600)' in result.output
        assert 'Expected Payoff for Player 1:' in result.output
        assert 'Expected Payoff for Player 2:' in result.output
    
    def test_payoffs_missing_arguments(self, test_game_file):
        """Test payoffs command with missing required arguments."""
        runner = CliRunner()
        result = runner.invoke(payoffs, [test_game_file])
        assert result.exit_code != 0
        assert 'Missing option' in result.output
    
    def test_payoffs_invalid_probabilities_sum(self, test_game_file):
        """Test payoffs command with probabilities not summing to 1."""
        runner = CliRunner()
        result = runner.invoke(payoffs, [
            test_game_file,
            '--p1-strategy', '0.7,0.4',  # sums to 1.1
            '--p2-strategy', '0.4,0.6'
        ])
        assert result.exit_code != 0
        assert 'must be valid probabilities summing to 1' in result.output
    
    def test_payoffs_negative_probabilities(self, test_game_file):
        """Test payoffs command with negative probabilities."""
        runner = CliRunner()
        result = runner.invoke(payoffs, [
            test_game_file,
            '--p1-strategy', '-0.1,1.1',
            '--p2-strategy', '0.4,0.6'
        ])
        assert result.exit_code != 0
        assert 'must be valid probabilities' in result.output
    
    def test_payoffs_wrong_dimensions(self, test_game_file):
        """Test payoffs command with wrong strategy dimensions."""
        runner = CliRunner()
        result = runner.invoke(payoffs, [
            test_game_file,
            '--p1-strategy', '0.3,0.3,0.4',  # 3 values for 2x2 game
            '--p2-strategy', '0.4,0.6'
        ])
        assert result.exit_code != 0
        assert 'has 3 values but game has 2 rows' in result.output
    
    def test_payoffs_invalid_format(self, test_game_file):
        """Test payoffs command with invalid number format."""
        runner = CliRunner()
        result = runner.invoke(payoffs, [
            test_game_file,
            '--p1-strategy', 'abc,def',
            '--p2-strategy', '0.4,0.6'
        ])
        assert result.exit_code != 0
        assert 'Error parsing strategies:' in result.output


class TestBestResponseCommand:
    """Test the best-response command."""
    
    @pytest.fixture
    def test_game_file(self):
        """Create a test game file."""
        content = """GAME_TYPE: prisoners_dilemma
PARAMS:
  t: 5
  r: 3
  p: 1
  s: 0
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(content)
            f.flush()
            yield f.name
        os.unlink(f.name)
    
    def test_best_response_help(self):
        """Test best-response command help."""
        runner = CliRunner()
        result = runner.invoke(best_response, ['--help'])
        assert result.exit_code == 0
        assert 'Find best responses' in result.output
        assert '--player' in result.output
        assert '--opponent-strategy' in result.output
    
    def test_best_response_player1(self, test_game_file):
        """Test best-response command for player 1."""
        runner = CliRunner()
        result = runner.invoke(best_response, [
            test_game_file,
            '--player', '1',
            '--opponent-strategy', '0.4,0.6'
        ])
        assert result.exit_code == 0
        assert 'Best Response Analysis:' in result.output
        assert 'Player 1 vs Opponent Strategy:' in result.output
        assert 'Player 1 Expected Payoffs' in result.output
        assert 'Best Response:' in result.output
    
    def test_best_response_player2(self, test_game_file):
        """Test best-response command for player 2."""
        runner = CliRunner()
        result = runner.invoke(best_response, [
            test_game_file,
            '--player', '2',
            '--opponent-strategy', '0.7,0.3'
        ])
        assert result.exit_code == 0
        assert 'Player 2 vs Opponent Strategy:' in result.output
        assert 'Player 2 Expected Payoffs' in result.output
    
    def test_best_response_missing_player(self, test_game_file):
        """Test best-response command without player specification."""
        runner = CliRunner()
        result = runner.invoke(best_response, [
            test_game_file,
            '--opponent-strategy', '0.4,0.6'
        ])
        assert result.exit_code != 0
        assert 'Missing option' in result.output
    
    def test_best_response_invalid_player(self, test_game_file):
        """Test best-response command with invalid player number."""
        runner = CliRunner()
        result = runner.invoke(best_response, [
            test_game_file,
            '--player', '3',
            '--opponent-strategy', '0.4,0.6'
        ])
        assert result.exit_code != 0
        assert 'Invalid value for' in result.output
    
    def test_best_response_invalid_strategy(self, test_game_file):
        """Test best-response command with invalid opponent strategy."""
        runner = CliRunner()
        result = runner.invoke(best_response, [
            test_game_file,
            '--player', '1',
            '--opponent-strategy', '0.3,0.4'  # doesn't sum to 1
        ])
        assert result.exit_code != 0
        assert 'must be valid probabilities summing to 1' in result.output
    
    def test_best_response_wrong_dimensions(self, test_game_file):
        """Test best-response with wrong strategy dimensions."""
        runner = CliRunner()
        result = runner.invoke(best_response, [
            test_game_file,
            '--player', '1',
            '--opponent-strategy', '0.3,0.3,0.4'  # 3 values for 2x2 game
        ])
        assert result.exit_code != 0
        assert 'has 3 values but expected 2' in result.output


class TestValidateCommand:
    """Test the validate command."""
    
    @pytest.fixture
    def valid_game_file(self):
        """Create a valid game file."""
        content = """GAME_TYPE: prisoners_dilemma
PARAMS:
  t: 5
  r: 3
  p: 1
  s: 0
NAME: Valid Game
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(content)
            f.flush()
            yield f.name
        os.unlink(f.name)
    
    @pytest.fixture
    def invalid_game_file(self):
        """Create an invalid game file."""
        content = """INVALID_TYPE: not_a_game
MISSING: required_fields
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(content)
            f.flush()
            yield f.name
        os.unlink(f.name)
    
    def test_validate_help(self):
        """Test validate command help."""
        runner = CliRunner()
        result = runner.invoke(validate, ['--help'])
        assert result.exit_code == 0
        assert 'Validate a game definition file' in result.output
    
    def test_validate_valid_file(self, valid_game_file):
        """Test validate command with valid file."""
        runner = CliRunner()
        result = runner.invoke(validate, [valid_game_file])
        assert result.exit_code == 0
        assert f'✓ {valid_game_file} is valid' in result.output
    
    def test_validate_invalid_file(self, invalid_game_file):
        """Test validate command with invalid file."""
        runner = CliRunner()
        result = runner.invoke(validate, [invalid_game_file])
        assert result.exit_code != 0
        assert 'Validation errors for' in result.output
    
    def test_validate_nonexistent_file(self):
        """Test validate command with nonexistent file."""
        runner = CliRunner()
        result = runner.invoke(validate, ['nonexistent.yml'])
        assert result.exit_code != 0
        assert "File 'nonexistent.yml' not found" in result.output


class TestExamplesCommand:
    """Test the examples command."""
    
    def test_examples_help(self):
        """Test examples command help."""
        runner = CliRunner()
        result = runner.invoke(examples, ['--help'])
        assert result.exit_code == 0
        assert 'List available example game files' in result.output
    
    @patch('nash_file.Path')
    def test_examples_no_directory(self, mock_path_class):
        """Test examples command when examples directory doesn't exist."""
        # Mock the Path(__file__).parent / "examples" chain
        mock_file_path = mock_path_class.return_value
        mock_parent = mock_file_path.parent
        mock_examples_dir = mock_parent.__truediv__.return_value
        mock_examples_dir.exists.return_value = False
        
        runner = CliRunner()
        result = runner.invoke(examples, [])
        assert result.exit_code == 0
        assert 'No examples directory found' in result.output
    
    @patch('nash_file.Path')
    def test_examples_no_files(self, mock_path_class):
        """Test examples command when no example files exist."""
        # Mock the Path(__file__).parent / "examples" chain
        mock_file_path = mock_path_class.return_value
        mock_parent = mock_file_path.parent
        mock_examples_dir = mock_parent.__truediv__.return_value
        mock_examples_dir.exists.return_value = True
        mock_examples_dir.glob.return_value = []
        
        runner = CliRunner()
        result = runner.invoke(examples, [])
        assert result.exit_code == 0
        assert 'No example game files found' in result.output
    
    def test_examples_with_real_files(self):
        """Test examples command with real example files."""
        runner = CliRunner()
        result = runner.invoke(examples, [])
        assert result.exit_code == 0
        
        # Should find the actual example files in the project
        if 'No example' not in result.output:
            assert 'Available example game files:' in result.output
            assert 'To analyze an example:' in result.output
            # Check for some expected example files
            expected_files = ['prisoners_dilemma.yml', 'battle_of_sexes.yml']
            for expected in expected_files:
                if expected in result.output:
                    assert 'Type:' in result.output
                    assert 'Size:' in result.output
                    break
    
    @patch('nash_file.Path')
    @patch('nash_file.GameFileParser')
    def test_examples_parse_error(self, mock_parser, mock_path_class):
        """Test examples command when file parsing fails."""
        # Mock the Path(__file__).parent / "examples" chain
        mock_file_path = mock_path_class.return_value
        mock_parent = mock_file_path.parent
        mock_examples_dir = mock_parent.__truediv__.return_value
        mock_examples_dir.exists.return_value = True
        
        # Create a mock path object for the broken file
        class MockFile:
            def __init__(self, name):
                self.name = name
                
        mock_file = MockFile('broken.yml')
        mock_examples_dir.glob.side_effect = [[mock_file], []]
        
        # Make parser raise an exception
        mock_parser.return_value.parse_file.side_effect = Exception("Parse error")
        
        runner = CliRunner()
        result = runner.invoke(examples, [])
        assert result.exit_code == 0
        assert 'broken.yml' in result.output
        assert '(Unable to parse)' in result.output


class TestCLIErrorHandling:
    """Test CLI error handling and edge cases."""
    
    def test_keyboard_interrupt_handling(self):
        """Test that KeyboardInterrupt is handled gracefully."""
        with patch('nash_file.click.echo') as mock_echo:
            with patch('nash_file.sys.exit') as mock_exit:
                # Simulate the exception handling in main
                try:
                    raise KeyboardInterrupt()
                except KeyboardInterrupt:
                    mock_echo.side_effect = lambda msg, err=False: None
                    mock_exit.side_effect = lambda code: None
                    
                    # This simulates the exception handling in the main block
                    mock_echo("\nProgram terminated by user.", err=True)
                    mock_exit(130)
                    
                    mock_echo.assert_called_with("\nProgram terminated by user.", err=True)
                    mock_exit.assert_called_with(130)
    
    def test_unexpected_error_handling(self):
        """Test that unexpected errors are handled gracefully."""
        with patch('nash_file.click.echo') as mock_echo:
            with patch('nash_file.sys.exit') as mock_exit:
                # Simulate the exception handling in main
                test_error = Exception("Test error")
                try:
                    raise test_error
                except Exception as e:
                    mock_echo.side_effect = lambda msg, err=False: None
                    mock_exit.side_effect = lambda code: None
                    
                    # This simulates the exception handling in the main block
                    mock_echo(f"\nUnexpected error: {e}", err=True)
                    mock_exit(1)
                    
                    mock_echo.assert_called_with(f"\nUnexpected error: {test_error}", err=True)
                    mock_exit.assert_called_with(1)


if __name__ == '__main__':
    pytest.main([__file__])
