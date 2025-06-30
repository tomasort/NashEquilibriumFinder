# Nash Equilibrium Finder

**by Tomas Ortega and Pablo Mueller**

## Overview

Nash Equilibrium Finder is a Python-based tool for analyzing 2-player normal form games from game theory. It provides comprehensive functionality for game creation, analysis, and equilibrium finding with multiple interfaces for different use cases.

### Key Features

- **File-Based CLI**: Modern YAML-based game definition and analysis
- **Web API**: RESTful interface for web applications
- **Programmatic Library**: Use as a Python package in your projects
- **Game Types**: Support for common games (Prisoner's Dilemma, Battle of Sexes, etc.) and custom games
- **Nash Equilibrium Analysis**: Find both pure and mixed strategy equilibria
- **Comprehensive Analysis**: Best responses, expected payoffs, and more

### What You Can Do

- Create random or custom 2-player normal form games
- Find best responses for each player
- Identify pure strategy Nash equilibria
- Calculate mixed strategy Nash equilibria for 2x2 games
- Compute expected payoffs for mixed strategies
- Validate and analyze games from YAML files
- Export results to JSON format

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [File-Based CLI Usage](#file-based-cli-usage)
4. [YAML Game Format](#yaml-game-format)
5. [Web API](#web-api)
6. [Programmatic Usage](#programmatic-usage)
7. [Testing](#testing)
8. [Documentation](#documentation)
9. [Contributing](#contributing)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/username/NashEquilibriumFinder.git
cd NashEquilibriumFinder
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

The primary interface is the file-based CLI that uses YAML configuration files to define games. This approach provides:

- **Reusability**: Games can be saved, shared, and reused
- **Clarity**: YAML format is human-readable and self-documenting  
- **Version Control**: Game definitions can be tracked in git
- **Validation**: Files can be validated before analysis

### Basic Usage

```bash
# List available example games
python nash_file.py examples

# Analyze a game for Nash equilibria
python nash_file.py analyze examples/prisoners_dilemma.yml

# Calculate expected payoffs with mixed strategies
python nash_file.py payoffs examples/prisoners_dilemma.yml --p1-strategy 0.7,0.3 --p2-strategy 0.4,0.6

# Find best response against opponent's strategy
python nash_file.py best-response examples/battle_of_sexes.yml --player 1 --opponent-strategy 0.3,0.7

# Validate a game file format
python nash_file.py validate examples/market_competition.yml

# Get output in JSON format
python nash_file.py analyze examples/prisoners_dilemma.yml --output json
```

## File-Based CLI Usage

The file-based CLI (`nash_file.py`) is the recommended interface and provides these commands:

- `examples` - List available example games with descriptions
- `analyze [file]` - Complete Nash equilibrium analysis
- `validate [file]` - Validate YAML game file format  
- `payoffs [file]` - Calculate expected payoffs for mixed strategies
- `best-response [file]` - Find optimal responses to opponent strategies

All commands support multiple output formats:
- `--output normal` (default): Human-readable format
- `--output minimal`: Compact results only
- `--output json`: Machine-readable JSON format

For detailed help on any command:
```bash
python nash_file.py [command] --help
```

## YAML Game Format

Games are defined using YAML files with a clean, readable format. The system supports multiple game definition methods:

### Web API

To run the web API server:

```bash
python3 web_api.py
```

This will start a Flask server on http://127.0.0.1:5000/ with the following endpoints:

- `POST /api/games`: Create a new game
- `POST /api/common-games`: Create a common game type
- `GET /api/games/<game_id>`: Get a game by ID
- `GET /api/games/<game_id>/analyze`: Analyze a game for Nash equilibria
- `POST /api/games/<game_id>/expected-payoffs`: Calculate expected payoffs
- `GET /api/games/<game_id>/random-beliefs`: Generate random mixed strategies

### Programmatic Usage

To use the library in your own code:

```python
from normal_form.game_manager import GameManager

# Create a GameManager
gm = GameManager()

# Create a Prisoner's Dilemma game
game_id, game = gm.create_common_game('prisoners_dilemma')

# Print the game
print(game.get_formatted_normal_form())

# Find Nash equilibria
analysis = gm.analyze_game(game_id)
print(f"Nash equilibria at: {analysis['pure_nash']}")

# Export the game to JSON
json_output = gm.export_game(game_id, format='json')
```

The project includes demo scripts to showcase different usage patterns:

```bash
# Programmatic API demo
python3 demo_programmatic.py

# CLI interface demo
python3 demo_cli.py
```

### Common Game Types

```yaml
# Prisoner's Dilemma
GAME_TYPE: prisoners_dilemma
PARAMS:
  t: 5  # Temptation payoff
  r: 3  # Reward payoff  
  p: 1  # Punishment payoff
  s: 0  # Sucker payoff
NAME: Prisoner's Dilemma
DESCRIPTION: Classic game theory example
```

```yaml
# Custom game with explicit payoff matrix
GAME_TYPE: custom
PAYOFFS:
  - [(3,3), (0,5)]  # Row 1: (player1_payoff, player2_payoff)
  - [(5,0), (1,1)]  # Row 2: (player1_payoff, player2_payoff)
NAME: Custom Game
DESCRIPTION: Game with explicit payoffs
```

```yaml
# Randomly generated game
GAME_TYPE: random
STRATEGIES: 3 3  # rows columns (player1 strategies, player2 strategies)
RANGE: -10 10    # min max payoff values
NAME: Random Game
DESCRIPTION: Randomly generated payoffs
```

### Available Game Types

The system supports these predefined game types:

- `prisoners_dilemma` - Classic cooperation vs. defection
- `coordination` - Players benefit from coordinating
- `battle_of_sexes` - Coordination with conflicting preferences  
- `zero_sum` - One player's gain is another's loss
- `custom` - Define explicit payoff matrix
- `random` - Generate random payoffs

Example files are provided in the `examples/` directory demonstrating each format.

## Common Game Types

The system supports creating common game types with predefined parameters:

- **Prisoner's Dilemma**: `create_prisoners_dilemma(t=5, r=3, p=1, s=0)`
- **Coordination Game**: `create_coordination_game(a=5, b=3)`
- **Battle of the Sexes**: `create_battle_of_sexes(a=3, b=2)`
- **Zero-Sum Game**: `create_zero_sum_game(values=None)`

## Architecture

The project follows a clean, service-oriented architecture:

1. **Core Model**: `NormalForm` class implements game theory concepts
2. **Service Layer**: `GameManager` class provides a high-level API
3. **Interfaces**: CLI, Web API, and programmatic access
4. **Utilities**: Shared functions for formatting and display

## Constraints

- **Number of players**: Fixed at 2
- **Number of strategies**: 1 to n (technically unlimited)
- **Mixed strategy equilibrium**: Currently supports 2x2 games only

## Testing

The project includes a comprehensive test suite using pytest. To run the tests:

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the tests:

```bash
pytest
```

3. To run tests with coverage report:

```bash
pytest --cov=normal_form
```

## Advanced Features

### Strategy Dominance Analysis
```python
from normal_form import NormalForm

# Create a game
game = NormalForm(mode='d', payoff_matrix=[
    [(4,1), (0,0)], 
    [(3,0), (1,1)]
])

# Check for dominant strategies
player1_dominated = game.get_dominated_strategies(player=1)
print(f"Player 1 dominated strategies: {player1_dominated}")

# Check if a specific strategy is dominant
is_dominant = game.is_dominant_strategy(strategy_index=0, player=1)
print(f"Strategy A1 is dominant: {is_dominant}")
```

### Regret Analysis
```python
# Calculate regret for given strategies
p1_strategy = [0.6, 0.4]
p2_strategy = [0.3, 0.7]

p1_regret, p2_regret = game.calculate_regret(p1_strategy, p2_strategy)
print(f"Player 1 regret: {p1_regret:.3f}")
print(f"Player 2 regret: {p2_regret:.3f}")
```

### Performance Optimization
The library includes performance optimizations:
- Caching for expensive calculations
- Numpy integration for numerical operations
- Efficient algorithms for large games

### Type Hints and Validation
```python
# Input validation
try:
    game.validate_strategy([0.6, 0.3], player=1)  # Won't sum to 1
except ValueError as e:
    print(f"Invalid strategy: {e}")

# Game structure validation
game.validate_game_structure()
```

## Development

### Code Quality Tools
The project uses several code quality tools:

```bash
# Format code
black .

# Check style
flake8 .

# Type checking
mypy normal_form/

# Security analysis
bandit -r normal_form/
```

### Pre-commit Hooks
Install pre-commit hooks for automatic code quality checks:

```bash
pip install pre-commit
pre-commit install
```

### Performance Testing
Run performance tests:

```bash
pytest tests/test_performance.py -v
```

### Property-Based Testing
Run property-based tests with hypothesis:

```bash
pip install hypothesis
pytest tests/test_properties.py -v
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [API Reference](docs/api_reference.md) - Detailed method documentation
- [Examples](docs/examples.md) - Common game examples and analysis
- [Game Theory Concepts](docs/concepts.md) - Explanation of game theory concepts
- [Game Format Guide](docs/game_format.md) - YAML format specification
- [Workflow Guide](docs/workflow.md) - Visual usage guide
- [Extension Guide](docs/extending.md) - How to extend the library

For testing information, see the [Testing Guide](tests/README.md).
