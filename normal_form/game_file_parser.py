"""
Game File Parser

This module provides functionality to parse game definition files
and create NormalForm games from them.
"""

import re
import os
from typing import Dict, List, Tuple, Any, Optional
from normal_form.game_manager import GameManager


class GameFileParseError(Exception):
    """Exception raised when parsing a game file fails."""
    pass


class GameFileParser:
    """Parser for game definition files."""
    
    def __init__(self):
        """Initialize the parser."""
        self.game_manager = GameManager()
    
    def parse_file(self, file_path: str) -> Tuple[str, Any]:
        """
        Parse a game definition file and create a game.
        
        Arguments:
            file_path: Path to the game definition file
            
        Returns:
            Tuple of (game_id, game_object)
            
        Raises:
            GameFileParseError: If the file cannot be parsed
            FileNotFoundError: If the file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Game file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.parse_content(content, file_path)
    
    def parse_content(self, content: str, source_name: str = "<string>") -> Tuple[str, Any]:
        """
        Parse game definition content and create a game.
        
        Arguments:
            content: The game definition content
            source_name: Name/path of the source (for error messages)
            
        Returns:
            Tuple of (game_id, game_object)
            
        Raises:
            GameFileParseError: If the content cannot be parsed
        """
        try:
            game_def = self._parse_game_definition(content, source_name)
            return self._create_game_from_definition(game_def)
        except Exception as e:
            raise GameFileParseError(f"Error parsing {source_name}: {e}")
    
    def _parse_game_definition(self, content: str, source_name: str) -> Dict[str, Any]:
        """Parse the game definition content into a structured dictionary."""
        lines = content.split('\n')
        game_def = {
            'game_type': None,
            'strategies': None,
            'params': {},
            'payoffs': None,
            'player1_strategies': None,
            'player2_strategies': None,
            'name': None,
            'description': None
        }
        
        current_section = None
        payoff_matrix = []
        
        for line_num, original_line in enumerate(lines, 1):
            line = original_line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Check for section headers (top-level keys - no leading whitespace)
            if ':' in line and original_line[0] not in [' ', '\t']:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                # Strip inline comments
                if '#' in value:
                    value = value.split('#')[0].strip()
                
                if key == 'game_type':
                    game_def['game_type'] = value
                    current_section = None
                elif key == 'strategies':
                    try:
                        rows, cols = map(int, value.split())
                        game_def['strategies'] = (rows, cols)
                    except ValueError:
                        raise GameFileParseError(f"Line {line_num}: Invalid strategies format. Expected 'rows columns'")
                    current_section = None
                elif key == 'params':
                    current_section = 'params'
                elif key == 'payoffs':
                    current_section = 'payoffs'
                elif key == 'player1_strategies':
                    game_def['player1_strategies'] = [s.strip() for s in value.split(',')]
                    current_section = None
                elif key == 'player2_strategies':
                    game_def['player2_strategies'] = [s.strip() for s in value.split(',')]
                    current_section = None
                elif key == 'name':
                    game_def['name'] = value
                    current_section = None
                elif key == 'description':
                    game_def['description'] = value
                    current_section = None
                else:
                    raise GameFileParseError(f"Line {line_num}: Unknown key '{key}'")
            
            # Handle section content (indented lines)
            elif current_section == 'params' and ':' in line:
                param_key, param_value = line.split(':', 1)
                param_key = param_key.strip().lower()  # Make parameter keys case-insensitive
                param_value = param_value.strip()
                
                # Strip inline comments
                if '#' in param_value:
                    param_value = param_value.split('#')[0].strip()
                
                # Try to parse the value
                try:
                    # Check if it's a list format [1, 2, 3, 4]
                    if param_value.startswith('[') and param_value.endswith(']'):
                        # Parse as list
                        list_content = param_value[1:-1].strip()
                        if list_content:
                            values = [item.strip() for item in list_content.split(',')]
                            parsed_values = []
                            for val in values:
                                try:
                                    if '.' in val:
                                        parsed_values.append(float(val))
                                    else:
                                        parsed_values.append(int(val))
                                except ValueError:
                                    parsed_values.append(val)
                            game_def['params'][param_key] = parsed_values
                        else:
                            game_def['params'][param_key] = []
                    # Try to parse as number
                    elif '.' in param_value:
                        game_def['params'][param_key] = float(param_value)
                    else:
                        game_def['params'][param_key] = int(param_value)
                except ValueError:
                    game_def['params'][param_key] = param_value
            
            elif current_section == 'payoffs':
                # Parse payoff matrix row
                payoff_row = self._parse_payoff_row(line, line_num)
                payoff_matrix.append(payoff_row)
            
            elif line.strip():
                raise GameFileParseError(f"Line {line_num}: Unexpected content outside of section")
        
        if payoff_matrix:
            game_def['payoffs'] = payoff_matrix
        
        return game_def
    
    def _parse_payoff_row(self, line: str, line_num: int) -> List[Tuple[int, int]]:
        """Parse a single row of payoffs."""
        # Find all payoff pairs in the format (p1, p2)
        pattern = r'\(\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*\)'
        matches = re.findall(pattern, line)
        
        # Also check for malformed tuples (wrong number of elements)
        malformed_pattern = r'\(\s*([+-]?\d+(?:\s*,\s*[+-]?\d+)*)\s*\)'
        all_tuples = re.findall(malformed_pattern, line)
        
        for tuple_content in all_tuples:
            elements = [x.strip() for x in tuple_content.split(',')]
            if len(elements) != 2:
                raise GameFileParseError(f"Line {line_num}: Payoff pairs must have exactly 2 elements, found {len(elements)}")
        
        if not matches:
            raise GameFileParseError(f"Line {line_num}: No valid payoff pairs found. Expected format: (p1, p2)")
        
        payoffs = []
        for match in matches:
            try:
                p1, p2 = int(match[0]), int(match[1])
                payoffs.append((p1, p2))
            except ValueError:
                raise GameFileParseError(f"Line {line_num}: Invalid payoff values: {match}")
        
        return payoffs
    
    def _create_game_from_definition(self, game_def: Dict[str, Any]) -> Tuple[str, Any]:
        """Create a game from the parsed definition."""
        game_type = game_def['game_type']
        
        if not game_type:
            raise GameFileParseError("GAME_TYPE is required")
        
        # Normalize game type to lowercase and replace spaces/underscores
        normalized_game_type = game_type.lower().replace(' ', '_')
        
        if normalized_game_type in ['prisoners_dilemma', 'coordination', 'battle_of_sexes', 'zero_sum']:
            # Create common game type
            game_id, game = self.game_manager.create_common_game(normalized_game_type, **game_def['params'])
        
        elif normalized_game_type == 'custom':
            # Create custom game
            if not game_def['payoffs']:
                raise GameFileParseError("PAYOFFS section is required for custom games")
            
            payoff_matrix = game_def['payoffs']
            game_id, game = self.game_manager.create_game('d', payoff_matrix=payoff_matrix)
        
        elif normalized_game_type == 'random':
            # Create random game
            if not game_def['strategies']:
                raise GameFileParseError("STRATEGIES is required for random games")
            
            rows, cols = game_def['strategies']
            params = game_def['params']
            
            game_id, game = self.game_manager.create_game(
                'r', 
                rows=rows, 
                columns=cols,
                lower_limit=params.get('min_value', -99),
                upper_limit=params.get('max_value', 99)
            )
        
        else:
            raise GameFileParseError(f"Unknown game type: {game_type}")
        
        # Set custom strategy names if provided
        if game_def['player1_strategies']:
            if len(game_def['player1_strategies']) != game.rows:
                raise GameFileParseError(f"Number of Player 1 strategies ({len(game_def['player1_strategies'])}) "
                                       f"doesn't match game rows ({game.rows})")
            # Note: This would require adding a method to set strategy names in NormalForm
        
        if game_def['player2_strategies']:
            if len(game_def['player2_strategies']) != game.columns:
                raise GameFileParseError(f"Number of Player 2 strategies ({len(game_def['player2_strategies'])}) "
                                       f"doesn't match game columns ({game.columns})")
        
        return game_id, game
    
    def validate_file(self, file_path: str) -> List[str]:
        """
        Validate a game file and return any warnings or errors.
        
        Arguments:
            file_path: Path to the game definition file
            
        Returns:
            List of warning/error messages (empty if valid)
        """
        warnings = []
        
        try:
            self.parse_file(file_path)
        except GameFileParseError as e:
            warnings.append(f"Parse error: {e}")
        except FileNotFoundError as e:
            warnings.append(f"File error: {e}")
        except Exception as e:
            warnings.append(f"Unexpected error: {e}")
        
        return warnings


def parse_game_file(filename):
    """
    Simple function wrapper for parsing game files.
    
    Args:
        filename: Path to the game file (.yml or .yaml format)
        
    Returns:
        Tuple of (game_id, game_object)
        
    Raises:
        FileNotFoundError: If file doesn't exist
        GameFileParseError: If file format is invalid
    """
    parser = GameFileParser()
    return parser.parse_file(filename)
