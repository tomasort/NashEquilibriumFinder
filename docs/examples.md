# Nash Equilibrium Finder Examples

This document provides examples of common game theory scenarios and shows how to analyze them using the Nash Equilibrium Finder.

## Table of Contents

- [Prisoner's Dilemma](#prisoners-dilemma)
- [Coordination Game](#coordination-game)
- [Battle of the Sexes](#battle-of-the-sexes)
- [Zero-Sum Game](#zero-sum-game)
- [Game with Dominated Strategy](#game-with-dominated-strategy)

## Prisoner's Dilemma

In the Prisoner's Dilemma, two suspects have been arrested. Each has the option to cooperate (with the other prisoner) or defect (confess to the police).

### Game Setup

```python
from normal_form.NormalForm import NormalForm

# Create a game
game = NormalForm(mode='m', rows=2, columns=2)

# Set up payoffs manually
# [[(cooperate, cooperate), (cooperate, defect)],
#  [(defect, cooperate), (defect, defect)]]
game.grid = [[(3, 3), (0, 5)], 
            [(5, 0), (1, 1)]]
game.grid_pure_nash = [[(3, 3), (0, 5)], 
                      [(5, 0), (1, 1)]]

# Print the game
print("Prisoner's Dilemma:")
game.print_normal_form()
```

Output:
```
Prisoner's Dilemma:
	    B1			    B2			
A1	( 3,  3)		( 0,  5)		
A2	( 5,  0)		( 1,  1)		
```

### Analysis

```python
# Find best responses for each player
p1_br = game.find_br(player=1)
p2_br = game.find_br(player=2)

print(f"Player 1's best responses: {p1_br}")
print(f"Player 2's best responses: {p2_br}")

# Find Nash equilibria
nash_eq = game.find_pure_nash_equi()
print(f"Nash equilibria: {nash_eq}")
```

Output:
```
Player 1's best responses: [(0, 1), (1, 1)]  # Player 1 always prefers to defect
Player 2's best responses: [(1, 0), (1, 1)]  # Player 2 always prefers to defect
Nash equilibria: [(1, 1)]  # Both defecting is the only Nash equilibrium
```

## Coordination Game

In a coordination game, players benefit from choosing the same strategy.

### Game Setup

```python
# Create a game
game = NormalForm(mode='m', rows=2, columns=2)

# Set up payoffs manually
game.grid = [[(5, 5), (0, 0)], 
            [(0, 0), (3, 3)]]
game.grid_pure_nash = [[(5, 5), (0, 0)], 
                      [(0, 0), (3, 3)]]

# Print the game
print("Coordination Game:")
game.print_normal_form()
```

Output:
```
Coordination Game:
	    B1			    B2			
A1	( 5,  5)		( 0,  0)		
A2	( 0,  0)		( 3,  3)		
```

### Analysis

```python
# Find Nash equilibria
nash_eq = game.find_pure_nash_equi()
print(f"Nash equilibria: {nash_eq}")

# Calculate mixed strategy Nash equilibrium
mixed_nash = game.get_indifference_probabilities()
print(f"Mixed strategy Nash equilibrium probabilities: {mixed_nash}")
```

Output:
```
Nash equilibria: [(0, 0), (1, 1)]  # Both (A1,B1) and (A2,B2) are Nash equilibria
Mixed strategy Nash equilibrium probabilities: None  # None because pure Nash equilibria exist
```

## Battle of the Sexes

In Battle of the Sexes, two players prefer to coordinate but have different preferences over which activity to attend.

### Game Setup

```python
# Create a game
game = NormalForm(mode='m', rows=2, columns=2)

# Set up payoffs manually
game.grid = [[(3, 2), (0, 0)], 
            [(0, 0), (2, 3)]]
game.grid_pure_nash = [[(3, 2), (0, 0)], 
                      [(0, 0), (2, 3)]]

# Print the game
print("Battle of the Sexes:")
game.print_normal_form()
```

Output:
```
Battle of the Sexes:
	    B1			    B2			
A1	( 3,  2)		( 0,  0)		
A2	( 0,  0)		( 2,  3)		
```

### Analysis

```python
# Find Nash equilibria
nash_eq = game.find_pure_nash_equi()
print(f"Nash equilibria: {nash_eq}")

# Calculate mixed strategy Nash equilibrium
mixed_nash = game.get_indifference_probabilities()
if mixed_nash:
    print(f"Player 1's mixed strategy: {mixed_nash[0]}")
    print(f"Player 2's mixed strategy: {mixed_nash[1]}")

# Calculate expected payoffs with mixed strategies
beliefs = game.create_random_beliefs()
p1_eps = game.find_br(player=1, mixing=True, beliefs=beliefs[1])
p2_eps = game.find_br(player=2, mixing=True, beliefs=beliefs[0])

print(f"Player 1's expected payoffs against {beliefs[1]}: {p1_eps}")
print(f"Player 2's expected payoffs against {beliefs[0]}: {p2_eps}")

# Calculate expected payoffs when both players mix
both_mix_ep = game.ep_bpm(p1_beliefs=beliefs[0], p2_beliefs=beliefs[1])
print(f"Expected payoffs with both mixing: {both_mix_ep}")
```

## Zero-Sum Game

In a zero-sum game, one player's gain is exactly balanced by the other player's loss.

### Game Setup

```python
# Create a game
game = NormalForm(mode='m', rows=2, columns=2)

# Set up payoffs manually
game.grid = [[(5, -5), (-3, 3)], 
            [(-2, 2), (4, -4)]]
game.grid_pure_nash = [[(5, -5), (-3, 3)], 
                      [(-2, 2), (4, -4)]]

# Print the game
print("Zero-Sum Game:")
game.print_normal_form()
```

Output:
```
Zero-Sum Game:
	    B1			    B2			
A1	( 5, -5)		(-3,  3)		
A2	(-2,  2)		( 4, -4)		
```

### Analysis

```python
# Find Nash equilibria
nash_eq = game.find_pure_nash_equi()
print(f"Nash equilibria: {nash_eq}")

# Calculate mixed strategy Nash equilibrium
mixed_nash = game.get_indifference_probabilities()
if mixed_nash:
    print(f"Player 1's mixed strategy: {mixed_nash[0]}")
    print(f"Player 2's mixed strategy: {mixed_nash[1]}")
```

## Game with Dominated Strategy

A dominated strategy is one that is always worse than another strategy, regardless of what the opponent does.

### Game Setup

```python
# Create a game
game = NormalForm(mode='m', rows=2, columns=2)

# Set up payoffs manually - Row player's second strategy is dominated
game.grid = [[(5, 1), (3, 0)], 
            [(3, 2), (2, 1)]]
game.grid_pure_nash = [[(5, 1), (3, 0)], 
                      [(3, 2), (2, 1)]]

# Print the game
print("Game with Dominated Strategy:")
game.print_normal_form()
```

Output:
```
Game with Dominated Strategy:
	    B1			    B2			
A1	( 5,  1)		( 3,  0)		
A2	( 3,  2)		( 2,  1)		
```

### Analysis

```python
# Find best responses for each player
p1_br = game.find_br(player=1)
print(f"Player 1's best responses: {p1_br}")

# Find Nash equilibria
nash_eq = game.find_pure_nash_equi()
print(f"Nash equilibria: {nash_eq}")
```

Output:
```
Player 1's best responses: [(0, 0), (0, 1)]  # Player 1 always prefers A1 (row 1)
Nash equilibria: [(0, 0)]  # (A1, B1) is the Nash equilibrium
```
