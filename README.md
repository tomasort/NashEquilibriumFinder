# Nash Equilibrium Finder

## by Tomas Ortega and Pablo Mueller
   
## What is Nash Equilibrium Finder?

Nash Equilibrium Finder is a Python-based tool that allows you to analyze 2-player normal form games from game theory. It provides functionality to:

- Create random or custom 2-player normal form games
- Find best responses for each player
- Identify pure strategy Nash equilibria
- Calculate mixed strategy Nash equilibria for 2x2 games
- Compute expected payoffs for mixed strategies
- Generate random belief vectors (mixed strategies)

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

To run the interactive mode:

```bash
python3 main.py
```

To use the library in your own code:

```python
from normal_form.NormalForm import NormalForm

# Create a 2x2 game (Prisoner's Dilemma)
game = NormalForm(mode='m', rows=2, columns=2)  # 'm' for manual entry
game.grid = [[(3, 3), (0, 5)], 
            [(5, 0), (1, 1)]]
game.grid_pure_nash = [[(3, 3), (0, 5)], 
                      [(5, 0), (1, 1)]]

# Print the game
game.print_normal_form()

# Find Nash equilibria
nash_eq = game.find_pure_nash_equi()
print(f"Nash equilibria at: {nash_eq}")
```

## Constraints

- Number of players: Fixed at 2
- Number of strategies (rows/columns): 1 to n (technically unlimited)
- For mixed strategy equilibrium calculations: Currently only supports 2x2 games

## Documentation

Comprehensive documentation is available in the `docs` directory:

- [Documentation Home](docs/index.md) - Overview, installation, and basic usage
- [API Reference](docs/api_reference.md) - Detailed method documentation
- [Examples](docs/examples.md) - Common game examples and their analysis
- [Game Theory Concepts](docs/concepts.md) - Explanation of relevant game theory concepts

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

For more details on testing, see the [Testing Guide](tests/README.md).

## Quick Demo

[Video demonstration](https://youtu.be/pFt3PR78Oh8)
