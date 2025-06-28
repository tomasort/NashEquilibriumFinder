# Nash Equilibrium Finder Workflow

This document provides a visual guide to using the Nash Equilibrium Finder to analyze games.

## Analysis Flowchart

```
┌───────────────────┐
│ Create Game       │
│ NormalForm(mode,  │
│ rows, columns)    │
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│ Add Payoffs       │
│ game.add_payoffs()│
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│ Display Game      │
│ game.print_normal_│
│ form()            │
└───────┬───────────┘
        │
        ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ Find Pure Nash    │    │ Calculate Mixed   │    │ Calculate         │
│ Equilibria        │───▶│ Strategy Nash     │───▶│ Expected Payoffs  │
│ game.find_pure_   │    │ Equilibrium       │    │ game.ep_bpm()     │
│ nash_equi()       │    │ game.get_         │    │                   │
└───────────────────┘    │ indifference_     │    └───────────────────┘
                         │ probabilities()   │
                         └───────────────────┘
                         
```

## Step-by-Step Process

1. **Create a Normal Form Game**
   - Specify mode ('r' for random, 'm' for manual)
   - Define number of rows (player 1 strategies)
   - Define number of columns (player 2 strategies)

2. **Add Payoffs**
   - For random mode: payoffs are generated automatically
   - For manual mode: enter payoffs for each cell

3. **Display the Game**
   - View the normal form representation

4. **Find Pure Strategy Nash Equilibria**
   - Get the coordinates of all pure Nash equilibria
   - If none exist, proceed to mixed strategies

5. **Calculate Mixed Strategy Nash Equilibrium (for 2×2 games)**
   - Get the probability distribution for each player
   - Returns `None` if pure Nash equilibria exist

6. **Calculate Expected Payoffs**
   - For one player using a mixed strategy
   - For both players using mixed strategies

## Example Code

```python
from normal_form.NormalForm import NormalForm

# Step 1: Create a game
game = NormalForm(mode='r', rows=2, columns=2)

# Step 2: Add payoffs
game.add_payoffs()

# Step 3: Display the game
print("Game in normal form:")
game.print_normal_form()

# Step 4: Find pure Nash equilibria
nash_eq = game.find_pure_nash_equi()
print(f"Pure Nash equilibria: {nash_eq}")

# Step 5: Calculate mixed strategy Nash equilibrium (if no pure Nash)
if len(nash_eq) == 0:
    mixed_nash = game.get_indifference_probabilities()
    if mixed_nash:
        print(f"Mixed strategy Nash equilibrium:")
        print(f"Player 1: {mixed_nash[0]}")
        print(f"Player 2: {mixed_nash[1]}")

# Step 6: Calculate expected payoffs
# Create random beliefs (mixed strategies)
beliefs = game.create_random_beliefs()
p1_ep, p2_ep = game.ep_bpm(beliefs[0], beliefs[1])
print(f"Expected payoff for Player 1: {p1_ep}")
print(f"Expected payoff for Player 2: {p2_ep}")
```
