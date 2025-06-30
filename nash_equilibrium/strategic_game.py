#  =============================================================================
#  Group Number: 30
#
# PROGRAMMER1: Tomas Ortega
#  PANTHER  ID1: 5677483

# PROGRAMMER2: Pablo Mueller
#   PANTHER ID2: 3283876

#   CLASS: CAP4506
#   SECTION: U01
#   SEMESTER: Spring 2019
#   CLASSTIME: M / W  6:25 - 7:45 PM

#   Project: This program will alow the user to find nash equilibriums and calculate expected payoffs for each player.
#   DUE: Sunday, Apruk  7,  2019 at midnight.

#   CERTIFICATION: I certify    that    this    work    is  my own  and that none   of it is the work of any other  person.
#  =============================================================================

import functools
import random
from typing import List, Tuple

import numpy as np

# Factory methods for common games


def create_prisoners_dilemma(t=5, r=3, p=1, s=0):
    """Create a Prisoner's Dilemma game.

    In Prisoner's Dilemma, T > R > P > S and 2R > T + S

    Arguments:
        t: Temptation payoff (defect while other cooperates)
        r: Reward payoff (both cooperate)
        p: Punishment payoff (both defect)
        s: Sucker payoff (cooperate while other defects)

    Returns:
        NormalForm object representing the Prisoner's Dilemma
    """
    if not (t > r > p > s and 2 * r > t + s):
        raise ValueError("Invalid parameters for Prisoner's Dilemma. Must satisfy T > R > P > S and 2R > T + S")

    payoff_matrix = [[(r, r), (s, t)], [(t, s), (p, p)]]

    return StrategicGame(mode="d", payoff_matrix=payoff_matrix)


def create_coordination_game(a=5, b=3):
    """Create a Coordination Game.

    In a Coordination Game, players benefit from choosing the same strategy.

    Arguments:
        a: Payoff for first coordination option (both choose A1, B1)
        b: Payoff for second coordination option (both choose A2, B2)

    Returns:
        NormalForm object representing the Coordination Game
    """
    if a <= 0 or b <= 0:
        raise ValueError("Parameters a and b must be positive")

    payoff_matrix = [[(a, a), (0, 0)], [(0, 0), (b, b)]]

    return StrategicGame(mode="d", payoff_matrix=payoff_matrix)


def create_battle_of_sexes(a=3, b=2):
    """Create a Battle of the Sexes game.

    In Battle of the Sexes, players prefer to coordinate but have different preferences.

    Arguments:
        a: Preferred payoff (a > b)
        b: Secondary payoff

    Returns:
        NormalForm object representing the Battle of the Sexes
    """
    if not (a > b > 0):
        raise ValueError("Parameters must satisfy a > b > 0")

    payoff_matrix = [[(a, b), (0, 0)], [(0, 0), (b, a)]]

    return StrategicGame(mode="d", payoff_matrix=payoff_matrix)


def create_zero_sum_game(values=None):
    """Create a Zero - Sum Game.

    Arguments:
        values: Optional list of values for player 1. Player 2 gets negative of these values.
               If not provided, random values are generated.

    Returns:
        NormalForm object representing a Zero - Sum Game
    """
    if values is None:
        values = [random.randint(-5, 5) for _ in range(4)]

    if len(values) != 4:
        raise ValueError("Must provide exactly 4 values")

    payoff_matrix = [
        [(values[0], -values[0]), (values[1], -values[1])],
        [(values[2], -values[2]), (values[3], -values[3])],
    ]

    return StrategicGame(mode="d", payoff_matrix=payoff_matrix)


class StrategicGame:
    def __init__(self, mode="d", rows=None, columns=None, payoff_matrix=None, lower_limit=-99, upper_limit=99):
        """ Initialize a grid that represents the normal form of a game

            Arguments:
            mode: 'r' for random, 'm' for manual input, or 'd' for direct payoff matrix.
                  If 'r' then values are generated in the range (lower_limit, upper_limit).
                  If 'd' then payoff_matrix must be provided.
            rows: number of rows in the normal form grid (strategies for player 1)
            columns: number of columns in the normal form grid (strategies for player 2)
            payoff_matrix: A list of lists containing tuples (p1_payoff, p2_payoff).
                          Required if mode is 'd'.
            lower_limit: lower limit for random payoffs if mode is 'r'
            upper_limit: upper limit for random payoffs if mode is 'r'

            Raises:
            ValueError: if mode is invalid or required parameters are missing
        """
        valid_modes = ["r", "m", "d"]
        if mode not in valid_modes:
            raise ValueError(f"Mode must be one of {valid_modes}")

        self.mode = mode
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

        # Handle direct payoff matrix initialization
        if mode == "d":
            if payoff_matrix is None:
                raise ValueError("payoff_matrix must be provided when mode is 'd'")

            self.grid = payoff_matrix
            self.rows = len(payoff_matrix)
            self.columns = len(payoff_matrix[0]) if self.rows > 0 else 0
            self.grid_pure_nash = [[payoff for payoff in row] for row in payoff_matrix]
        else:
            # Handle traditional initialization
            if rows is None or columns is None:
                raise ValueError("rows and columns must be provided when mode is 'r' or 'm'")

            self.rows = rows
            self.columns = columns
            # a list of lists for the rows and columns in the normal form
            self.grid = [[(0, 0) for i in range(self.columns)] for j in range(self.rows)]
            self.grid_pure_nash = [[(0, 0) for i in range(self.columns)] for j in range(self.rows)]

        # a list of tuples that represent the x and y coordinates each nash equilibrium
        self.nash_equilibria = []
        self.p1_br = []  # the set of best responses for player 1
        self.p2_br = []  # the set of best responses for player 2

    def get_payoffs(self, player):
        """Get the payoffs for a specific player as a list.

        Arguments:
            player: The player number (1 or 2)

        Returns:
            List of payoffs for the specified player

        Raises:
            ValueError: If player is not 1 or 2
        """
        if player == 1:
            return [[col[0] for col in row] for row in self.grid]
        elif player == 2:
            return [[col[1] for col in row] for row in self.grid]
        else:
            raise ValueError("There are only two players")

    def get_formatted_payoffs(self, player):
        """Get the payoffs for a specific player as a formatted string.

        Arguments:
            player: The player number (1 or 2)

        Returns:
            String containing formatted payoffs

        Raises:
            ValueError: If player is not 1 or 2
        """
        payoffs = ""
        count = 1
        num_rows = 7
        if player == 1:
            for rows in self.grid:
                for col in rows:
                    value = str(col[0])
                    if len(value) == 1:
                        value = "  " + value
                    elif len(value) == 2:
                        value = " " + value
                    if count == num_rows:
                        payoffs += str(value) + "\n"
                        count = 0
                    else:
                        payoffs += str(value) + " "
                    count += 1
        elif player == 2:
            for rows in self.grid:
                for col in rows:
                    value = str(col[1])
                    if len(value) == 1:
                        value = "  " + value
                    elif len(value) == 2:
                        value = " " + value
                    if count == num_rows:
                        payoffs += str(value) + "\n"
                        count = 0
                    else:
                        payoffs += str(value) + " "
                    count += 1
        else:
            raise ValueError("There are only two players")
        return payoffs

    # We need to fix the format in this function.
    def print_payoffs(self, player):
        """Print the payoffs for a specific player.

        Arguments:
            player: The player number (1 or 2)

        Raises:
            ValueError: If player is not 1 or 2
        """
        print(self.get_formatted_payoffs(player))

    def get_strategies(self, player):
        """Get the list of strategies for a specific player.

        Arguments:
            player: The player number (1 or 2)

        Returns:
            List of strategy names for the specified player

        Raises:
            ValueError: If player is not 1 or 2
        """
        if player == 1:
            return [f"A{i + 1}" for i in range(self.rows)]
        elif player == 2:
            return [f"B{i + 1}" for i in range(self.columns)]
        else:
            raise ValueError("There are only 2 players")

    def get_formatted_strategies(self, player):
        """Get the strategies for a specific player as a formatted string.

        Arguments:
            player: The player number (1 or 2)

        Returns:
            String containing formatted strategies

        Raises:
            ValueError: If player is not 1 or 2
        """
        strategies = "{"
        if player == 1:
            for i in range(self.rows):
                if i == self.rows - 1:
                    strategies += f"A{i + 1}"
                else:
                    strategies += f"A{i + 1}, "
        elif player == 2:
            for i in range(self.columns):
                if i == self.columns - 1:
                    strategies += f"B{i + 1}"
                else:
                    strategies += f"B{i + 1}, "
        else:
            raise ValueError("There are only 2 players")
        strategies += "}"
        return strategies

    def print_strategies(self, player):
        """Print the strategies for a specific player.

        Arguments:
            player: The player number (1 or 2)

        Raises:
            ValueError: If player is not 1 or 2
        """
        # player 1 are rows and player 2 are the columns
        print(self.get_formatted_strategies(player))

    def get_normal_form_data(self):
        """Get the normal form game data as a structured dictionary.

        Returns:
            A dictionary containing the complete game information:
            {
                'header': ['B1', 'B2', ...],
                'rows': [
                    {'name': 'A1', 'payoffs': [(p1, p2), ...],
                    ...
                ]
            }
        """
        header = [f"B{i + 1}" for i in range(self.columns)]
        rows = []
        for r in range(self.rows):
            row_data = {"name": f"A{r + 1}", "payoffs": self.grid[r]}
            rows.append(row_data)

        return {"header": header, "rows": rows}

    def get_formatted_normal_form(self):
        """Get the normal form representation as a formatted string.

        Returns:
            String containing the formatted normal form game
        """
        result = []

        # Header
        columns = "\t"
        for i in range(self.columns):
            columns += f"    B{i + 1}\t\t\t"
        result.append(columns)

        # Rows
        r = 1
        for row in self.grid:
            row_string = f"A{r}\t"
            for c in row:
                new_value_x = str(c[0])
                new_value_y = str(c[1])

                while len(new_value_x) < 3:
                    new_value_x = " " + new_value_x
                while len(new_value_y) < 3:
                    new_value_y = " " + new_value_y
                row_string += f"({new_value_x}, {new_value_y})\t\t"
            r += 1
            result.append(row_string)

        return "\n".join(result)

    def print_normal_form(self):
        """Print the normal form representation of the game."""
        print(self.get_formatted_normal_form())

    def set_payoff(self, row, col, p1_payoff, p2_payoff):
        """Set payoff for a specific cell in the game grid.

        Arguments:
            row: Row index (0 - based)
            col: Column index (0 - based)
            p1_payoff: Payoff for player 1
            p2_payoff: Payoff for player 2

        Raises:
            IndexError: If row or col are out of bounds
        """
        if row < 0 or row >= self.rows:
            raise IndexError(f"Row index {row} out of bounds (0-{self.rows - 1})")
        if col < 0 or col >= self.columns:
            raise IndexError(f"Column index {col} out of bounds (0-{self.columns - 1})")

        self.grid[row][col] = (p1_payoff, p2_payoff)
        self.grid_pure_nash[row][col] = (p1_payoff, p2_payoff)

    def add_payoffs(self, input_function=None):
        """Add payoffs to the game grid.

        For mode 'r', random payoffs are generated.
        For mode 'm', payoffs are entered manually using the provided input_function
        or standard input if none is provided.
        For mode 'd', this method does nothing as payoffs are provided at initialization.

        Arguments:
            input_function: Optional function to get user input (for testing / UI abstraction)
                           If not provided, the built - in input() function is used.

        Raises:
            ValueError: If mode is not valid
        """
        if self.mode == "d":
            # Payoffs already set during initialization
            return

        # Default to standard input if no input_function is provided
        if input_function is None:
            input_function = input

        # this is just a counter for displaying the cells in the normal form as A1, A2, ...
        r = 0
        for row in self.grid:
            c = 0
            for column in row:
                if self.mode == "r":
                    p1 = random.randint(self.lower_limit, self.upper_limit)
                    p2 = random.randint(self.lower_limit, self.upper_limit)
                    self.grid[r][c] = (p1, p2)
                    self.grid_pure_nash[r][c] = (p1, p2)
                elif self.mode == "m":
                    payoff = input_function(f"Enter payoff for ( A{r + 1}, B{c + 1} ) = ")
                    values = payoff.split(",")
                    try:
                        p1 = int(values[0])
                        p2 = int(values[1])
                        self.grid[r][c] = (p1, p2)
                        self.grid_pure_nash[r][c] = (p1, p2)
                    except (ValueError, IndexError):
                        raise ValueError("Payoff must be two comma - separated integers (e.g., 3, 4)")
                else:
                    raise ValueError(f"Invalid mode: {self.mode}")
                c += 1
            r += 1

    def calculate_best_responses(self, player, update_state=False):
        """Calculate best responses for a player without modifying class state.

        Arguments:
            player: The player number (1 or 2)
            update_state: Whether to update the class state (for backward compatibility)

        Returns:
            A list of (column, row) coordinates representing best responses

        Raises:
            ValueError: If player is not 1 or 2
        """
        if player != 1 and player != 2:
            raise ValueError("player must be an int with the value of 1 or 2")

        best_responses = []
        grid_pure_nash_copy = [[payoff for payoff in row] for row in self.grid_pure_nash]

        if player == 1:
            for i in range(self.columns):
                br_coordinates = best = None
                counter = 0
                multiple_br_values = []
                for row in self.grid:
                    current_value = row[i][player - 1]
                    # in x, y format (columns, row)
                    current_value_coordinates = (i, counter)
                    if best is None or current_value > best:
                        best = current_value
                        br_coordinates = current_value_coordinates
                    elif best == current_value:
                        if current_value_coordinates not in multiple_br_values:
                            multiple_br_values.append(current_value_coordinates)
                    counter += 1

                if br_coordinates not in multiple_br_values:
                    multiple_br_values.append(br_coordinates)

                for coordinates in multiple_br_values:
                    if update_state:
                        c = self.grid_pure_nash[coordinates[1]][coordinates[0]]
                        self.grid_pure_nash[coordinates[1]][coordinates[0]] = ("H", c[1])
                    else:
                        c = grid_pure_nash_copy[coordinates[1]][coordinates[0]]
                        grid_pure_nash_copy[coordinates[1]][coordinates[0]] = ("H", c[1])

                for value in multiple_br_values:
                    if value not in best_responses:
                        best_responses.append(value)
                    if update_state and value not in self.p1_br:
                        self.p1_br.append(value)

        elif player == 2:
            counter = 0
            for row in self.grid:
                br_coordinates = best = None
                multiple_br_values = []
                for i in range(self.columns):
                    current_value = row[i][player - 1]
                    # in x, y format (columns, row)
                    current_value_coordinates = (i, counter)
                    if best is None or current_value > best:
                        best = current_value
                        br_coordinates = current_value_coordinates
                    elif best == current_value:
                        if current_value_coordinates not in multiple_br_values:
                            multiple_br_values.append(current_value_coordinates)
                counter += 1

                if br_coordinates not in multiple_br_values:
                    multiple_br_values.append(br_coordinates)

                for coordinates in multiple_br_values:
                    if update_state:
                        c = self.grid_pure_nash[coordinates[1]][coordinates[0]]
                        self.grid_pure_nash[coordinates[1]][coordinates[0]] = (c[0], "H")
                    else:
                        c = grid_pure_nash_copy[coordinates[1]][coordinates[0]]
                        grid_pure_nash_copy[coordinates[1]][coordinates[0]] = (c[0], "H")

                for value in multiple_br_values:
                    if value not in best_responses:
                        best_responses.append(value)
                    if update_state and value not in self.p2_br:
                        self.p2_br.append(value)

        return best_responses

    def calculate_expected_payoffs(self, player, beliefs):
        """Calculate expected payoffs for a player against a mixed strategy.

        Arguments:
            player: The player number (1 or 2)
            beliefs: The opponent's mixed strategy (list of probabilities)

        Returns:
            A dictionary mapping strategy names to expected payoffs

        Raises:
            ValueError: If player is not 1 or 2
        """
        if player != 1 and player != 2:
            raise ValueError("player must be an int with the value of 1 or 2")

        expected_payoffs = {}

        if player == 1:
            for i in range(self.rows):
                result = 0
                for j in range(self.columns):
                    result += beliefs[j] * self.grid[i][j][player - 1]
                key = f"A{i + 1}"
                expected_payoffs[key] = result

        elif player == 2:
            for i in range(self.columns):
                counter = 0
                result = 0
                for row in self.grid:
                    p2_payoff = row[i][1]
                    b = beliefs[counter]
                    result += b * p2_payoff
                    counter += 1
                key = f"B{i + 1}"
                expected_payoffs[key] = result

        return expected_payoffs

    # Maybe use for i in range(self.row) instead of for l in self.grid
    def find_br(self, player, mixing=False, beliefs=None):
        """Finds all the best responses of the specified player.

        This function supports both pure strategy best responses and
        best responses against mixed strategies.

        Arguments:
            player: (1 or 2) The player for whom to find best responses
            mixing: (boolean) Whether the opponent is using a mixed strategy
            beliefs: The opponent's mixed strategy (required if mixing = True)

        Returns:
            If mixing = False: A list of (column, row) coordinates
            If mixing = True: A dictionary mapping strategy names to expected payoffs

        Raises:
            ValueError: If player is not 1 or 2 or if mixing = True but beliefs not provided
        """
        if mixing and beliefs is None:
            raise ValueError("beliefs must be provided when mixing = True")

        if not mixing:
            # For backward compatibility, update class state
            return self.calculate_best_responses(player, update_state=True)
        else:
            return self.calculate_expected_payoffs(player, beliefs)

    def find_pure_nash_equi(self, update_state=True):
        """Find all pure strategy Nash equilibria.

        A pure strategy Nash equilibrium is a strategy profile where neither
        player has an incentive to deviate unilaterally.

        Arguments:
            update_state: Whether to update the class state (for backward compatibility)

        Returns:
            A list of (column, row) coordinates representing Nash equilibria
        """
        # Get best responses for both players
        player1 = self.calculate_best_responses(player=1, update_state=update_state)
        player2 = self.calculate_best_responses(player=2, update_state=update_state)

        # Nash equilibria are cells that are best responses for both players
        nash_eq = [value for value in player1 if value in player2]

        # Update class state if requested
        if update_state:
            self.nash_equilibria = nash_eq

        return nash_eq

    def create_random_beliefs(self, mode="dirichlet"):
        if mode == "dirichlet":
            # We can use the Dirichlet distribution https://en.wikipedia.org / wiki/Dirichlet_distribution
            p1_beliefs = np.random.dirichlet(np.ones(self.rows), size=1).tolist()[
                0
            ]  # we need the [0] because it is a list of lists
            p2_beliefs = np.random.dirichlet(np.ones(self.columns), size=1).tolist()[0]
        elif mode == "sum":
            # Or we can create a random array of numbers, then get the sum and divide every number by the sum
            p1_rand_numbers = [random.random() for i in range(self.rows)]
            s = sum(p1_rand_numbers)
            p1_beliefs = [round(i / s, 3) for i in p1_rand_numbers]

            p2_rand_numbers = [random.random() for i in range(self.columns)]
            s = sum(p2_rand_numbers)
            p2_beliefs = [round(i / s, 3) for i in p2_rand_numbers]
        return [p1_beliefs, p2_beliefs]

    def get_pure_nash_data(self):
        """Get the normal form with Nash equilibria highlighted as structured data.

        Returns:
            A dictionary containing the complete game information with Nash equilibria:
            {
                'header': ['B1', 'B2', ...],
                'rows': [
                    {'name': 'A1', 'payoffs': [(p1, p2), ...],
                    ...
                ],
                'nash_equilibria': [(col, row), ...]
            }
        """
        header = [f"B{i + 1}" for i in range(self.columns)]
        rows = []
        for r in range(self.rows):
            row_data = {"name": f"A{r + 1}", "payoffs": self.grid_pure_nash[r]}
            rows.append(row_data)

        return {"header": header, "rows": rows, "nash_equilibria": self.nash_equilibria}

    def get_formatted_pure_nash(self):
        """Get the normal form with Nash equilibria highlighted as a formatted string.

        Returns:
            String containing the formatted normal form with Nash equilibria
        """
        result = []

        # Header
        columns = "\t"
        for i in range(self.columns):
            columns += f"    B{i + 1}\t\t\t"
        result.append(columns)

        # Rows
        r = 1
        for row in self.grid_pure_nash:
            row_string = f"A{r}\t"
            for c in row:
                new_value_x = str(c[0])
                new_value_y = str(c[1])

                while len(new_value_x) < 3:
                    new_value_x = " " + new_value_x
                while len(new_value_y) < 3:
                    new_value_y = " " + new_value_y

                row_string += f"({new_value_x}, {new_value_y})\t\t"
            r += 1
            result.append(row_string)

        return "\n".join(result)

    def print_pure_nash(self):
        """Print the normal form with Nash equilibria highlighted."""
        print(self.get_formatted_pure_nash())

    def ep_bpm(self, p1_beliefs, p2_beliefs):
        """Calculate expected payoffs when both players use mixed strategies.

        Arguments:
            p1_beliefs: List of probabilities for Player 1's strategies
            p2_beliefs: List of probabilities for Player 2's strategies

        Returns:
            Tuple of expected payoffs (p1_payoff, p2_payoff)

        Raises:
            ValueError: If belief vectors don't match game dimensions
        """
        if len(p1_beliefs) != self.rows:
            raise ValueError(f"p1_beliefs must have length {self.rows}")
        if len(p2_beliefs) != self.columns:
            raise ValueError(f"p2_beliefs must have length {self.columns}")

        # We need to create another grid with the product of the beliefs
        beliefs = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(p1_beliefs[i] * p2_beliefs[j])
            beliefs.append(row)

        # Now we need to do some kind of matrix multiplication between beliefs and self.grid
        # We start with player 1
        p1_ep = 0
        for i in range(self.rows):
            for j in range(self.columns):
                x = beliefs[i][j]
                y = self.grid[i][j][0]
                p1_ep += x * y

        p2_ep = 0
        for i in range(self.rows):
            for j in range(self.columns):
                p2_ep += beliefs[i][j] * self.grid[i][j][1]

        return p1_ep, p2_ep

    def to_dict(self):
        """Convert the game to a dictionary representation for serialization.

        Returns:
            Dictionary containing all game information
        """
        # Basic game information
        result = {
            "rows": self.rows,
            "columns": self.columns,
            "mode": self.mode,
            "payoff_matrix": self.grid,
            "p1_strategies": self.get_strategies(1),
            "p2_strategies": self.get_strategies(2),
            "p1_payoffs": self.get_payoffs(1),
            "p2_payoffs": self.get_payoffs(2),
            "nash_equilibria": self.nash_equilibria,
        }

        # Calculate pure Nash equilibria if not done yet
        if not self.nash_equilibria:
            result["nash_equilibria"] = self.find_pure_nash_equi(update_state=False)

        # For 2x2 games, include mixed strategy Nash equilibrium
        if self.rows == 2 and self.columns == 2:
            mixed_result = self.get_indifference_probabilities(check_pure_nash=False)
            if isinstance(mixed_result, dict):
                result["mixed_strategy"] = {
                    "p1_strategy": mixed_result.get("p1_strategy"),
                    "p2_strategy": mixed_result.get("p2_strategy"),
                    "error": mixed_result.get("error"),
                }
            else:
                # Handle legacy return format
                result["mixed_strategy"] = {
                    "p1_strategy": mixed_result[0] if mixed_result else None,
                    "p2_strategy": mixed_result[1] if mixed_result else None,
                    "error": None,
                }

        return result

    def get_indifference_probabilities(self, check_pure_nash=True):
        """Calculate the mixed strategy Nash equilibrium for a 2x2 game.

        Arguments:
            check_pure_nash: If True, check for pure Nash equilibria first

        Returns:
            A dictionary with mixed strategies and any error messages:
            {
                'p1_strategy': [p, 1 - p],  # Player 1's mixed strategy
                'p2_strategy': [q, 1 - q],  # Player 2's mixed strategy
                'error': None or error message
            }

        Raises:
            ValueError: If game is not 2x2
        """
        # Check if we have a 2x2 game
        if self.rows != 2 or self.columns != 2:
            raise ValueError("Mixed strategy calculation only supported for 2x2 games")

        # Check for pure Nash equilibria
        if check_pure_nash:
            # Use the existing nash_equilibria if it's been calculated
            # otherwise calculate it without updating state
            nash_eq = self.nash_equilibria if self.nash_equilibria else self.find_pure_nash_equi(update_state=False)
            if nash_eq:
                return {
                    "p1_strategy": None,
                    "p2_strategy": None,
                    "error": "Pure Nash equilibria exist, no need for mixed strategy",
                }

        result = {"p1_strategy": None, "p2_strategy": None, "error": None}

        # Calculate Player 1's mixed strategy
        # (that makes Player 2 indifferent)
        x = self.grid[0][0][1]
        y = self.grid[1][0][1]
        z = self.grid[0][1][1]
        w = self.grid[1][1][1]

        denominator1 = x - y + w - z
        if denominator1 != 0:
            p = (w - y) / denominator1
            if p < 0 or (1 - p) < 0:
                result["error"] = "Negative probabilities for Player 1. One or more strategies may be dominated."
                return result
        else:
            result[
                "error"
            ] = "Division by zero when calculating Player 1's strategy. One or more strategies may be dominated."
            return result

        # Calculate Player 2's mixed strategy
        # (that makes Player 1 indifferent)
        x = self.grid[0][0][0]
        y = self.grid[1][0][0]
        z = self.grid[0][1][0]
        w = self.grid[1][1][0]

        denominator2 = x - y + w - z
        if denominator2 != 0:
            q = (w - z) / denominator2
            if q < 0 or (1 - q) < 0:
                result["error"] = "Negative probabilities for Player 2. One or more strategies may be dominated."
                return result
        else:
            result[
                "error"
            ] = "Division by zero when calculating Player 2's strategy. One or more strategies may be dominated."
            return result

        result["p1_strategy"] = [p, 1 - p]
        result["p2_strategy"] = [q, 1 - q]

        # For backward compatibility, we'll still return the old format
        # if there's no error
        if check_pure_nash:
            # For backward compatibility
            return [result["p1_strategy"], result["p2_strategy"]]
        else:
            return result

    def __str__(self):
        """Return a string representation of the game."""
        return f"NormalForm({self.rows}x{self.columns}, mode='{self.mode}')"

    def __repr__(self):
        """Return a detailed string representation of the game."""
        return f"NormalForm(mode='{self.mode}', rows={self.rows}, columns={self.columns})"

    def __eq__(self, other):
        """Check equality between two StrategicGame games."""
        if not isinstance(other, StrategicGame):
            return False
        return self.grid == other.grid and self.rows == other.rows and self.columns == other.columns

    def validate_strategy(self, strategy, player):
        """Validate that a strategy is valid for the given player.

        Arguments:
            strategy: List of probabilities representing a mixed strategy
            player: Player number (1 or 2)

        Returns:
            bool: True if strategy is valid

        Raises:
            ValueError: If strategy is invalid
        """
        if player not in [1, 2]:
            raise ValueError("Player must be 1 or 2")

        expected_length = self.rows if player == 1 else self.columns
        if len(strategy) != expected_length:
            raise ValueError(f"Strategy for player {player} must have {expected_length} elements")

        if not all(0 <= prob <= 1 for prob in strategy):
            raise ValueError("All probabilities must be between 0 and 1")

        if abs(sum(strategy) - 1.0) > 1e-6:
            raise ValueError(f"Strategy probabilities must sum to 1, got {sum(strategy)}")

        return True

    def validate_game_structure(self):
        """Validate that the game structure is consistent.

        Returns:
            bool: True if game structure is valid

        Raises:
            ValueError: If game structure is invalid
        """
        if self.rows <= 0 or self.columns <= 0:
            raise ValueError("Game must have at least one row and one column")

        if len(self.grid) != self.rows:
            raise ValueError(f"Grid has {len(self.grid)} rows but should have {self.rows}")

        for i, row in enumerate(self.grid):
            if len(row) != self.columns:
                raise ValueError(f"Row {i} has {len(row)} columns but should have {self.columns}")

            for j, cell in enumerate(row):
                if not isinstance(cell, tuple) or len(cell) != 2:
                    raise ValueError(f"Cell ({i}, {j}) must be a tuple of length 2")

        return True

    # Cache for expensive computations
    @functools.lru_cache(maxsize=128)
    def _cached_expected_payoff(payoffs_tuple: Tuple, p1_strategy: Tuple, p2_strategy: Tuple):
        """Cached version of expected payoff calculation."""
        payoffs = [list(row) for row in payoffs_tuple]
        p1_strat = list(p1_strategy)
        p2_strat = list(p2_strategy)

        p1_ep = 0
        p2_ep = 0

        for i in range(len(payoffs)):
            for j in range(len(payoffs[0])):
                prob = p1_strat[i] * p2_strat[j]
                p1_ep += prob * payoffs[i][j][0]
                p2_ep += prob * payoffs[i][j][1]

        return p1_ep, p2_ep

    def is_dominant_strategy(self, strategy_index: int, player: int, strict: bool = True):
        """Check if a strategy is dominant for a player.

        Args:
            strategy_index: Index of the strategy to check
            player: Player number (1 or 2)
            strict: Whether to check for strict dominance (default) or weak dominance

        Returns:
            bool: True if the strategy is dominant
        """
        if player == 1:
            strategies = range(self.rows)
            other_player_strategies = range(self.columns)
        else:
            strategies = range(self.columns)
            other_player_strategies = range(self.rows)

        # Check against all other strategies
        for other_strat in strategies:
            if other_strat == strategy_index:
                continue

            dominates = True
            for opp_strat in other_player_strategies:
                if player == 1:
                    payoff1 = self.grid[strategy_index][opp_strat][0]
                    payoff2 = self.grid[other_strat][opp_strat][0]
                else:
                    payoff1 = self.grid[opp_strat][strategy_index][1]
                    payoff2 = self.grid[opp_strat][other_strat][1]

                if strict and payoff1 <= payoff2:
                    dominates = False
                    break
                elif not strict and payoff1 < payoff2:
                    dominates = False
                    break

            if not dominates:
                return False

        return True

    def get_dominated_strategies(self, player: int, strict: bool = True):
        """Get all dominated strategies for a player.

        Args:
            player: Player number (1 or 2)
            strict: Whether to check for strict dominance (default) or weak dominance

        Returns:
            List of dominated strategy indices
        """
        dominated = []
        strategies = range(self.rows if player == 1 else self.columns)

        for strat in strategies:
            if not self.is_dominant_strategy(strat, player, strict):
                # Check if this strategy is dominated by any other
                for other_strat in strategies:
                    if other_strat != strat:
                        if self._is_dominated_by(strat, other_strat, player, strict):
                            dominated.append(strat)
                            break

        return dominated

    def _is_dominated_by(self, strategy1: int, strategy2: int, player: int, strict: bool):
        """Check if strategy1 is dominated by strategy2."""
        other_player_strategies = range(self.columns if player == 1 else self.rows)

        for opp_strat in other_player_strategies:
            if player == 1:
                payoff1 = self.grid[strategy1][opp_strat][0]
                payoff2 = self.grid[strategy2][opp_strat][0]
            else:
                payoff1 = self.grid[opp_strat][strategy1][1]
                payoff2 = self.grid[opp_strat][strategy2][1]

            if strict and payoff1 >= payoff2:
                return False
            elif not strict and payoff1 > payoff2:
                return False

        return True

    def calculate_regret(self, p1_strategy: List[float], p2_strategy: List[float]):
        """Calculate regret for both players given their strategies.

        Args:
            p1_strategy: Player 1's mixed strategy
            p2_strategy: Player 2's mixed strategy

        Returns:
            Tuple of (p1_regret, p2_regret)
        """
        # Current expected payoffs
        current_p1, current_p2 = self.ep_bpm(p1_strategy, p2_strategy)

        # Best response payoffs
        p1_best_responses = self.find_br(1, mixing=True, beliefs=p2_strategy)
        p2_best_responses = self.find_br(2, mixing=True, beliefs=p1_strategy)

        # Calculate maximum possible payoffs
        if isinstance(p1_best_responses, dict):
            max_p1_payoff = max(p1_best_responses.values())
        else:
            # Calculate payoffs for pure best responses
            max_p1_payoff = current_p1  # Fallback

        if isinstance(p2_best_responses, dict):
            max_p2_payoff = max(p2_best_responses.values())
        else:
            max_p2_payoff = current_p2  # Fallback

        p1_regret = max_p1_payoff - current_p1
        p2_regret = max_p2_payoff - current_p2

        return p1_regret, p2_regret
