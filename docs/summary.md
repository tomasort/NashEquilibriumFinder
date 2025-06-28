# Nash Equilibrium Finder Documentation Summary

This document provides an overview of all available documentation for the Nash Equilibrium Finder project.

## Documentation Structure

The documentation for Nash Equilibrium Finder is organized into several sections:

1. **[Documentation Home](index.md)**: Overview of the project, installation instructions, and basic usage.

2. **[API Reference](api_reference.md)**: Detailed documentation of all classes and methods, including parameters, return values, and examples.

3. **[Examples](examples.md)**: Examples of common game theory scenarios (Prisoner's Dilemma, Coordination Game, etc.) and how to analyze them using Nash Equilibrium Finder.

4. **[Game Theory Concepts](concepts.md)**: Explanations of key game theory concepts relevant to the project, such as Nash equilibrium, best response, mixed strategies, etc.

5. **[Workflow Guide](workflow.md)**: A visual guide showing the typical workflow for analyzing games with Nash Equilibrium Finder.

6. **[Extension Guide](extending.md)**: Information for developers on how to extend the Nash Equilibrium Finder with new functionality.

7. **[Testing Guide](../tests/README.md)**: Guide to the testing infrastructure, including running tests and adding new tests.

## Quick Reference

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from normal_form.NormalForm import NormalForm

# Create a game
game = NormalForm(mode='r', rows=2, columns=2)

# Add payoffs
game.add_payoffs()

# Print the game
game.print_normal_form()

# Find Nash equilibria
nash_eq = game.find_pure_nash_equi()
```

### Key Methods

- `NormalForm(mode, rows, columns)`: Create a new game
- `add_payoffs()`: Set payoffs for the game
- `print_normal_form()`: Display the game
- `find_br(player, mixing, beliefs)`: Find best responses
- `find_pure_nash_equi()`: Find pure strategy Nash equilibria
- `get_indifference_probabilities()`: Calculate mixed strategy Nash equilibrium
- `ep_bpm(p1_beliefs, p2_beliefs)`: Calculate expected payoffs with mixed strategies
- `create_random_beliefs(mode)`: Generate random mixed strategies

## Document Relationships

```
                  ┌─────────────┐
                  │  index.md   │
                  │ (Main Page) │
                  └──────┬──────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
┌────────▼────────┐ ┌────▼─────┐ ┌───────▼────────┐
│   api_reference  │ │ examples │ │    concepts    │
│       .md       │ │   .md    │ │      .md       │
└─────────────────┘ └──────────┘ └────────────────┘
         │               │               │
         └───────┐ ┌─────┘               │
                 │ │                     │
          ┌──────▼─▼──────┐     ┌────────▼────────┐
          │   workflow    │     │    extending    │
          │     .md      │     │      .md        │
          └──────────────┘     └─────────────────┘
```

## Additional Resources

- **[Project README](../README.md)**: Project overview and quick start guide
- **[GitHub Repository](https://github.com/username/NashEquilibriumFinder)**: Source code and issue tracking
- **[Video Demo](https://youtu.be/pFt3PR78Oh8)**: Video demonstration of the tool
