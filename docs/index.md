# Nash Equilibrium Finder - Documentation

This documentation provides detailed information about the Nash Equilibrium Finder project, including its architecture, key classes, methods, and usage examples.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [API Reference](#api-reference)
5. [Examples](#examples)
6. [Game Theory Concepts](#game-theory-concepts)
7. [Workflow](#workflow)
8. [Extending the Library](#extending-the-library)
9. [Testing](#testing)
10. [Documentation Summary](#documentation-summary)
11. [Contributing](#contributing)

## Overview

Nash Equilibrium Finder is a Python library that provides tools for creating and analyzing normal form games in game theory. It can find pure strategy Nash equilibria, calculate mixed strategy Nash equilibria, and compute expected payoffs.

Key features include:
- Create random or manually specified normal form games
- Find best responses for each player
- Identify pure strategy Nash equilibria
- Calculate mixed strategy Nash equilibria
- Compute expected payoffs for mixed strategies

## Installation

To install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Basic usage of the Nash Equilibrium Finder:

```python
from normal_form.NormalForm import NormalForm

# Create a 2x2 normal form game
game = NormalForm(mode='r', rows=2, columns=2)

# Generate random payoffs
game.add_payoffs()

# Print the normal form representation
game.print_normal_form()

# Find pure strategy Nash equilibria
nash_equilibria = game.find_pure_nash_equi()
print(f"Nash equilibria: {nash_equilibria}")

# If no pure Nash equilibria, calculate mixed strategy Nash equilibrium
if len(nash_equilibria) == 0:
    mixed_nash = game.get_indifference_probabilities()
    print(f"Mixed strategy Nash equilibrium: {mixed_nash}")
```

## API Reference

See the detailed [API Reference](api_reference.md) for complete documentation of all classes and methods.

## Examples

For examples of common game theory scenarios and how to analyze them with Nash Equilibrium Finder, see the [Examples](examples.md) document.

## Game Theory Concepts

For explanations of key game theory concepts used in this project, see the [Game Theory Concepts](concepts.md) guide.

## Workflow

For a visual guide to analyzing games with Nash Equilibrium Finder, see the [Workflow Guide](workflow.md).

## Extending the Library

For information on how to extend Nash Equilibrium Finder with new functionality, see the [Extension Guide](extending.md).

## Documentation Summary

For a complete overview of all available documentation, see the [Documentation Summary](summary.md).
