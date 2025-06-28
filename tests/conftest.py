import pytest
import sys
import os

# Add the project root directory to the Python path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from normal_form.NormalForm import NormalForm

@pytest.fixture
def prisoners_dilemma():
    """
    Create a Prisoner's Dilemma game:
    
    | (R,R) | (S,T) |
    | (T,S) | (P,P) |
    
    Where T > R > P > S and 2R > T + S
    Using: T=5, R=3, P=1, S=0
    """
    game = NormalForm(mode='m', rows=2, columns=2)
    
    # Set up the grid manually (bypassing input)
    game.grid = [[(3, 3), (0, 5)], 
                [(5, 0), (1, 1)]]
    
    # Set up the grid_pure_nash with the same values
    game.grid_pure_nash = [[(3, 3), (0, 5)], 
                          [(5, 0), (1, 1)]]
    
    return game

@pytest.fixture
def coordination_game():
    """
    Create a Coordination Game:
    
    | (a,a) | (0,0) |
    | (0,0) | (b,b) |
    
    Where a > 0, b > 0
    Using a=5, b=3
    """
    game = NormalForm(mode='m', rows=2, columns=2)
    
    # Set up the grid manually
    game.grid = [[(5, 5), (0, 0)], 
                [(0, 0), (3, 3)]]
    
    # Set up the grid_pure_nash with the same values
    game.grid_pure_nash = [[(5, 5), (0, 0)], 
                          [(0, 0), (3, 3)]]
    
    return game

@pytest.fixture
def battle_of_sexes():
    """
    Create a Battle of the Sexes game:
    
    | (a,b) | (0,0) |
    | (0,0) | (b,a) |
    
    Where a > b > 0
    Using a=3, b=2
    """
    game = NormalForm(mode='m', rows=2, columns=2)
    
    # Set up the grid manually
    game.grid = [[(3, 2), (0, 0)], 
                [(0, 0), (2, 3)]]
    
    # Set up the grid_pure_nash with the same values
    game.grid_pure_nash = [[(3, 2), (0, 0)], 
                          [(0, 0), (2, 3)]]
    
    return game

@pytest.fixture
def zero_sum_game():
    """
    Create a Zero-Sum Game:
    
    | (a,-a) | (b,-b) |
    | (c,-c) | (d,-d) |
    
    Using a=5, b=-3, c=-2, d=4
    """
    game = NormalForm(mode='m', rows=2, columns=2)
    
    # Set up the grid manually
    game.grid = [[(5, -5), (-3, 3)], 
                [(-2, 2), (4, -4)]]
    
    # Set up the grid_pure_nash with the same values
    game.grid_pure_nash = [[(5, -5), (-3, 3)], 
                          [(-2, 2), (4, -4)]]
    
    return game

@pytest.fixture
def dominated_strategy_game():
    """
    Create a game with a dominated strategy:
    
    | (5,1) | (3,0) |
    | (3,2) | (2,1) |
    
    Row player's second strategy is dominated
    """
    game = NormalForm(mode='m', rows=2, columns=2)
    
    # Set up the grid manually
    game.grid = [[(5, 1), (3, 0)], 
                [(3, 2), (2, 1)]]
    
    # Set up the grid_pure_nash with the same values
    game.grid_pure_nash = [[(5, 1), (3, 0)], 
                          [(3, 2), (2, 1)]]
    
    return game
