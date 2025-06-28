# Extending Nash Equilibrium Finder

This guide provides information for developers who want to extend the Nash Equilibrium Finder library with new functionality.

## Table of Contents

- [Project Structure](#project-structure)
- [Adding New Game Types](#adding-new-game-types)
- [Adding New Analysis Methods](#adding-new-analysis-methods)
- [Testing New Functionality](#testing-new-functionality)
- [Documentation Guidelines](#documentation-guidelines)

## Project Structure

The Nash Equilibrium Finder project is organized as follows:

```
NashEquilibriumFinder/
├── normal_form/               # Main package
│   ├── __init__.py
│   └── NormalForm.py          # Core class implementation
├── tests/                     # Test directory
│   ├── __init__.py
│   ├── conftest.py            # Test fixtures
│   ├── test_normal_form.py    # Test cases
│   └── README.md              # Testing guide
├── docs/                      # Documentation
│   ├── index.md
│   ├── api_reference.md
│   ├── examples.md
│   └── ...
├── main.py                    # CLI interface
├── requirements.txt           # Dependencies
└── README.md                  # Main readme
```

## Adding New Game Types

To add support for new types of games, you can either:

1. Extend the `NormalForm` class with new methods, or
2. Create a new class that inherits from `NormalForm`

### Example: Adding Support for Extensive Form Games

```python
class ExtensiveFormGame(NormalForm):
    def __init__(self, num_players, max_depth, branching_factor):
        # Initialize with appropriate parameters
        super().__init__(mode='m', rows=2, columns=2)  # Base initialization
        self.num_players = num_players
        self.max_depth = max_depth
        self.branching_factor = branching_factor
        self.game_tree = self._build_game_tree()
        
    def _build_game_tree(self):
        # Implementation to build game tree structure
        pass
        
    def convert_to_normal_form(self):
        # Algorithm to convert extensive form to normal form
        # Updates self.grid and self.grid_pure_nash
        pass
        
    def find_subgame_perfect_equilibrium(self):
        # Method to find subgame perfect equilibria
        pass
```

## Adding New Analysis Methods

To add new analysis methods to the existing `NormalForm` class:

1. Add the method to `NormalForm.py`
2. Document the method with a docstring
3. Add tests for the new method

### Example: Adding a Method for Evolutionary Stable Strategies

```python
def is_evolutionary_stable(self, strategy, epsilon=1e-6):
    """Determines if a given strategy is evolutionary stable.
    
    A strategy is evolutionary stable if, once established, 
    it cannot be invaded by a small number of mutants with a different strategy.
    
    Args:
        strategy: List of probabilities representing a mixed strategy
        epsilon: The threshold for numerical comparisons
        
    Returns:
        bool: True if the strategy is evolutionary stable, False otherwise
    """
    # Implementation
    pass
```

## Testing New Functionality

When adding new functionality:

1. Create test fixtures in `conftest.py` if needed
2. Add test methods to appropriate test classes in `test_normal_form.py`
3. Run tests using `pytest` to verify

### Example: Test for New Method

```python
def test_is_evolutionary_stable(self, battle_of_sexes):
    # Mixed Nash equilibrium for Battle of Sexes is [0.6, 0.4], [0.4, 0.6]
    mixed_nash = battle_of_sexes.get_indifference_probabilities()
    
    # Test if this equilibrium is evolutionary stable
    assert battle_of_sexes.is_evolutionary_stable(mixed_nash[0]) is True
    
    # Test a non-stable strategy
    assert battle_of_sexes.is_evolutionary_stable([0.8, 0.2]) is False
```

## Documentation Guidelines

When extending the library, follow these documentation guidelines:

1. **Docstrings**: All methods should have docstrings following this format:
   ```python
   def method_name(self, param1, param2):
       """Short description.
       
       More detailed description.
       
       Args:
           param1: Description of param1
           param2: Description of param2
           
       Returns:
           Description of return value
           
       Raises:
           ExceptionType: When and why exception is raised
       """
   ```

2. **Update API Reference**: Add your new methods to `docs/api_reference.md`

3. **Add Examples**: If applicable, add example usage to `docs/examples.md`

4. **Update Concepts**: If introducing new concepts, add explanations to `docs/concepts.md`
