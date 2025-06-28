# Game Theory Concepts

This document explains key game theory concepts related to the Nash Equilibrium Finder project.

## Table of Contents

- [Normal Form Games](#normal-form-games)
- [Nash Equilibrium](#nash-equilibrium)
- [Pure vs. Mixed Strategies](#pure-vs-mixed-strategies)
- [Best Response](#best-response)
- [Dominated Strategies](#dominated-strategies)
- [Common Game Types](#common-game-types)

## Normal Form Games

A normal form game (also called a strategic form game) is a representation of a game using a matrix. For a 2-player game, the matrix has:

- Rows representing the strategies of player 1
- Columns representing the strategies of player 2
- Each cell containing a pair of payoffs (a, b) where:
  - a is the payoff to player 1
  - b is the payoff to player 2

In the Nash Equilibrium Finder, a 2×2 game might look like:

```
     Player 2
     B1    B2
    -------------
A1 | (3,3) | (0,5) |  Player 1
    -------------
A2 | (5,0) | (1,1) |
    -------------
```

Where A1, A2 are player 1's strategies, and B1, B2 are player 2's strategies.

## Nash Equilibrium

A Nash equilibrium is a set of strategies, one for each player, such that no player has an incentive to unilaterally change their strategy. In other words, each player's strategy is the best response to the other players' strategies.

For example, in the Prisoner's Dilemma:

```
        Cooperate    Defect
       ------------------------
Cooperate | (3,3)    | (0,5) |
       ------------------------
Defect    | (5,0)    | (1,1) |
       ------------------------
```

The only Nash equilibrium is (Defect, Defect) with payoffs (1,1), because:
- If player 1 plays Defect, player 2's best response is Defect
- If player 2 plays Defect, player 1's best response is Defect

## Pure vs. Mixed Strategies

### Pure Strategy

A pure strategy is when a player chooses a specific action with certainty (probability 1). For example, in Rock-Paper-Scissors, choosing Rock is a pure strategy.

### Mixed Strategy

A mixed strategy is a probability distribution over pure strategies. For example, in Rock-Paper-Scissors, playing Rock with probability 1/3, Paper with probability 1/3, and Scissors with probability 1/3 is a mixed strategy.

In Nash Equilibrium Finder, mixed strategies are represented as lists of probabilities. For example, if Player 1 has two strategies, [0.6, 0.4] means they play strategy 1 with 60% probability and strategy 2 with 40% probability.

## Best Response

A best response is a strategy that produces the most favorable outcome for a player, given the strategies of the other players.

In Nash Equilibrium Finder, the `find_br` method finds best responses:

- With `mixing=False`, it finds pure strategy best responses
- With `mixing=True`, it calculates expected payoffs against an opponent's mixed strategy

## Dominated Strategies

A strategy is dominated if there is another strategy that always provides a better payoff, regardless of what other players do.

- **Strictly dominated**: Strategy A is strictly dominated by strategy B if B always gives a strictly higher payoff than A.
- **Weakly dominated**: Strategy A is weakly dominated by strategy B if B always gives at least as high a payoff as A, and sometimes higher.

Rational players would never play strictly dominated strategies.

## Common Game Types

### Prisoner's Dilemma

A game where two players each have two options (cooperate or defect), and mutual cooperation is the socially optimal outcome, but mutual defection is the only Nash equilibrium.

### Coordination Game

A game where players benefit from making the same choice. Has multiple pure Nash equilibria.

### Battle of the Sexes

A coordination game where players prefer different equilibria but still want to coordinate.

### Zero-Sum Game

A game where one player's gain is exactly balanced by the other player's loss. The sum of payoffs in each cell equals zero.

### Games with Dominated Strategies

Games where at least one player has a dominated strategy, which a rational player would never choose.
