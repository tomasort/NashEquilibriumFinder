# API Reference

This document provides detailed information about the classes and methods in the Nash Equilibrium Finder project.

## Table of Contents

- [NormalForm Class](#normalform-class)
  - [Constructor](#constructor)
  - [Methods](#methods)
    - [add_payoffs](#add_payoffs)
    - [find_br](#find_br)
    - [find_pure_nash_equi](#find_pure_nash_equi)
    - [get_indifference_probabilities](#get_indifference_probabilities)
    - [ep_bpm](#ep_bpm)
    - [create_random_beliefs](#create_random_beliefs)
    - [Utility Methods](#utility-methods)

## NormalForm Class

The `NormalForm` class is the main class in the project, representing a normal form game with payoff matrices for two players.

### Constructor

```python
def __init__(self, mode, rows, columns, lower_limit=-99, upper_limit=99)
```

Initialize a grid that represents the normal form of a game.

**Arguments:**
- `mode`: 'r' for random or 'm' for manual. If 'r' then values are generated in the range (lower_limit, upper_limit)
- `rows`: number of rows in the normal form grid (the number of strategies for player 1)
- `columns`: number of columns in the normal form grid (the number of strategies for player 2)
- `lower_limit`: lower limit for the random values for payoffs if the mode is set to random (default: -99)
- `upper_limit`: upper limit for the random values for payoffs if the mode is set to random (default: 99)

**Raises:**
- `ValueError`: if mode is not 'r' or 'm'

**Example:**
```python
# Create a 2x2 game with random payoffs between -10 and 10
game = NormalForm(mode='r', rows=2, columns=2, lower_limit=-10, upper_limit=10)

# Create a 3x2 game with manually entered payoffs
game = NormalForm(mode='m', rows=3, columns=2)
```

### Methods

#### add_payoffs

```python
def add_payoffs(self)
```

Adds payoffs to the game grid. If mode is 'r', random payoffs are generated. If mode is 'm', payoffs are manually entered by the user.

**Example:**
```python
game = NormalForm(mode='r', rows=2, columns=2)
game.add_payoffs()  # Fills grid with random payoffs
```

#### find_br

```python
def find_br(self, player, mixing=False, beliefs=None)
```

Finds all the best responses of the specified player.

**Arguments:**
- `player`: (1 or 2) specifies the player for whom we find best responses
- `mixing`: (boolean) if True, calculate best responses against a mixed strategy; if False, find pure strategy best responses
- `beliefs`: The opponent's mixed strategy (required if mixing=True)

**Returns:**
- If mixing=False: A list of tuples representing coordinates of the best responses
- If mixing=True: A dictionary mapping strategy names to expected payoffs

**Example:**
```python
# Find pure strategy best responses for player 1
p1_best_responses = game.find_br(player=1)

# Find best response for player 2 against player 1's mixed strategy [0.6, 0.4]
p2_expected_payoffs = game.find_br(player=2, mixing=True, beliefs=[0.6, 0.4])
```

#### find_pure_nash_equi

```python
def find_pure_nash_equi(self)
```

Find all pure strategy Nash equilibria in the game.

**Returns:**
- A list of coordinate tuples representing the pure Nash equilibria

**Example:**
```python
nash_equilibria = game.find_pure_nash_equi()
print(f"Nash equilibria found at: {nash_equilibria}")
```

#### get_indifference_probabilities

```python
def get_indifference_probabilities(self)
```

Calculate the mixed strategy Nash equilibrium for a 2x2 game.

**Returns:**
- A list of two lists with mixed strategy probabilities for each player, or None if pure Nash equilibria exist

**Example:**
```python
mixed_nash = game.get_indifference_probabilities()
if mixed_nash:
    p1_strategy, p2_strategy = mixed_nash
    print(f"Player 1's mixed strategy: {p1_strategy}")
    print(f"Player 2's mixed strategy: {p2_strategy}")
```

#### ep_bpm

```python
def ep_bpm(self, p1_beliefs, p2_beliefs)
```

Calculate the expected payoffs when both players use mixed strategies.

**Arguments:**
- `p1_beliefs`: List of probabilities for player 1's strategies
- `p2_beliefs`: List of probabilities for player 2's strategies

**Returns:**
- A tuple (p1_ep, p2_ep) with the expected payoffs for each player

**Example:**
```python
p1_strategy = [0.6, 0.4]  # Player 1 plays strategy 1 with probability 0.6, strategy 2 with 0.4
p2_strategy = [0.3, 0.7]  # Player 2 plays strategy 1 with probability 0.3, strategy 2 with 0.7
p1_ep, p2_ep = game.ep_bpm(p1_strategy, p2_strategy)
print(f"Expected payoff for player 1: {p1_ep}")
print(f"Expected payoff for player 2: {p2_ep}")
```

#### create_random_beliefs

```python
def create_random_beliefs(self, mode='dirichlet')
```

Create random belief vectors (mixed strategies) for both players.

**Arguments:**
- `mode`: 'dirichlet' or 'sum' - method used to generate random probabilities

**Returns:**
- A list containing two lists: belief vectors for player 1 and player 2

**Example:**
```python
random_strategies = game.create_random_beliefs()
p1_strategy, p2_strategy = random_strategies
print(f"Random strategy for player 1: {p1_strategy}")
print(f"Random strategy for player 2: {p2_strategy}")
```

#### Utility Methods

The class also provides several utility methods for displaying information:

- `print_payoffs(player)`: Print payoffs for a specific player
- `print_strategies(player)`: Print strategy set for a specific player
- `print_normal_form()`: Print the normal form representation of the game
- `print_pure_nash()`: Print the grid with Nash equilibria highlighted
