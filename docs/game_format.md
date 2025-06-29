# Game Definition Format Specification

The Nash Equilibrium Finder supports a simple text-based format for defining games.

## Format Overview

```
# Comments start with #
GAME_TYPE: [prisoners_dilemma|coordination|battle_of_sexes|zero_sum|custom]
PLAYERS: 2
STRATEGIES: [rows] [columns]

# For common game types, you can specify parameters
PARAMS:
  param1: value1
  param2: value2

# For custom games, specify the payoff matrix
PAYOFFS:
  (p1_payoff, p2_payoff) (p1_payoff, p2_payoff) ...
  (p1_payoff, p2_payoff) (p1_payoff, p2_payoff) ...

# Optional: Strategy names (defaults to A1, A2, ... and B1, B2, ...)
PLAYER1_STRATEGIES: strategy1, strategy2, ...
PLAYER2_STRATEGIES: strategy1, strategy2, ...

# Optional: Game metadata
NAME: Game Name
DESCRIPTION: Game description
```

## Examples

### Prisoner's Dilemma
```
GAME_TYPE: prisoners_dilemma
PARAMS:
  t: 5
  r: 3
  p: 1
  s: 0
NAME: Prisoner's Dilemma
DESCRIPTION: Classic prisoner's dilemma game
```

### Custom 3x3 Game
```
GAME_TYPE: custom
STRATEGIES: 3 3
PAYOFFS:
  (3, 1) (0, 2) (1, 3)
  (2, 0) (1, 1) (0, 2)
  (1, 3) (2, 0) (3, 1)
PLAYER1_STRATEGIES: Attack, Defend, Retreat
PLAYER2_STRATEGIES: Aggressive, Moderate, Defensive
NAME: Military Strategy Game
DESCRIPTION: A strategic military engagement scenario
```

### Random Game Template
```
GAME_TYPE: random
STRATEGIES: 2 2
PARAMS:
  min_value: -10
  max_value: 10
NAME: Random 2x2 Game
```
