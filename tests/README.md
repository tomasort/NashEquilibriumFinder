# Nash Equilibrium Finder - Testing Guide

This directory contains the tests for the Nash Equilibrium Finder project. The tests are written using pytest.

## Setting Up for Testing

Before running tests, make sure you have the required packages:

```bash
pip install -r ../requirements.txt
```

## Running Tests

To run all tests:

```bash
pytest
```

To run tests with coverage report:

```bash
pytest --cov=normal_form
```

To generate an HTML coverage report:

```bash
pytest --cov=normal_form --cov-report=html
```

After running this command, you'll find the coverage report in the `htmlcov` directory.

## Test Categories

The tests are organized into several classes:

1. **TestNormalFormInitialization**: Tests for the initialization of the `NormalForm` class
2. **TestBestResponse**: Tests for the `find_br` method
3. **TestNashEquilibrium**: Tests for finding Nash equilibria
4. **TestExpectedPayoff**: Tests for expected payoff calculations
5. **TestIndifferenceProbabilities**: Tests for calculating mixed strategy Nash equilibrium
6. **TestRandomBeliefs**: Tests for creating random belief vectors

## Test Fixtures

Several common game scenarios are available as pytest fixtures:

- **prisoners_dilemma**: The classic Prisoner's Dilemma game
- **coordination_game**: A game with two coordination equilibria
- **battle_of_sexes**: Battle of the Sexes game
- **zero_sum_game**: A zero-sum game
- **dominated_strategy_game**: A game with a dominated strategy

You can use these fixtures in your own tests by adding them as parameters to your test functions.

## Adding New Tests

To add new tests:

1. Create a new test function inside the appropriate test class
2. Make sure the function name starts with `test_`
3. Use assertions to check expected results

Example:

```python
def test_my_new_feature(self, prisoners_dilemma):
    result = prisoners_dilemma.my_new_feature()
    assert result == expected_value
```
