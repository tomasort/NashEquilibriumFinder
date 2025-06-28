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
#   CLASSTIME: M/W  6:25-7:45 PM

#   Project: This program will alow the user to find nash equilibriums and calculate expected payoffs for each player.
#   DUE: Sunday, Apruk  7,  2019 at midnight.

#   CERTIFICATION: I certify    that    this    work    is  my own  and that none   of it is the work of any other  person.
#  =============================================================================

import random
import numpy as np 

class NormalForm():

    def __init__(self, mode, rows, columns, lower_limit=-99, upper_limit=99):
        """ Initialize a grid that represents the normal form of a game

            Arguments:
            mode: 'r' for random or 'm' for manual. If 'r' then we generate values in the range (lower_limit, upper_limit)
            rows: number of rows in the normal form grid (the number of strategies for player 1)
            columns: number of columns in the normal form grid (the number of strategies for player 2)
            lower_limit: lower limit for the random values for payoffs if the mode is set to random
            upper_limit: upper limit for the random values for payoffs if the mode is set to random
            
            Raises:
            ValueError: if mode is not 'r' or 'm'
        """
        if mode not in ['r', 'm']:
            raise ValueError("Mode must be 'r' for random or 'm' for manual")
            
        self.rows = rows
        self.columns = columns
        self.mode = mode
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        # a list of lists for the rows and columns in the normal form
        self.grid = [[(0, 0) for i in range(self.columns)]
                     for j in range(self.rows)]
        self.grid_pure_nash = [[(0, 0) for i in range(self.columns)]
                               for j in range(self.rows)]
        # a list of tuples that represent the x and y coordinates each nash equilibrium
        self.nash_equilibria = []
        self.p1_br = []  # the set of best responses for player 1
        self.p2_br = []  # the set of best responses for player 2

    # We need to fix the format in this function.
    def print_payoffs(self, player):
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
        print(payoffs)

    def print_strategies(self, player):
        # player 1 are rows and player 2 are the columns
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
        print(strategies)

    def print_normal_form(self):
        columns = "\t"
        for i in range(self.columns):
            columns += f"    B{i + 1}\t\t\t"
        print(columns)
        r = 1
        for row in self.grid:
            row_string = f"A{r}\t"
            for c in row:
                new_value_x = str(c[0])
                new_value_y = str(c[1])
                
                while len(new_value_x) < 3:
                    new_value_x = " "+ new_value_x
                while len(new_value_y) < 3:
                    new_value_y = " "+ new_value_y
                row_string += f"({new_value_x}, {new_value_y})\t\t"
            r += 1
            print(row_string)

    def add_payoffs(self):
        # this is just a counter for displaying the cells in the normal form as A1, A2, ...
        r = 0
        for row in self.grid:
            c = 0
            for column in row:
                if self.mode == 'r':
                    p1 = random.randint(self.lower_limit, self.upper_limit)
                    p2 = random.randint(self.lower_limit, self.upper_limit)
                    self.grid[r][c] = (p1, p2)
                    self.grid_pure_nash[r][c] = (p1, p2)
                elif self.mode == 'm':
                    
                    payoff = input(
                        f"Enter payoff for ( A{r + 1}, B{c + 1} ) = ")
                    values = payoff.split(',')
                    self.grid[r][c] = (int(values[0]), int(values[1]))
                    self.grid_pure_nash[r][c] = (
                        int(values[0]), int(values[1]))
                else:
                    raise ValueError
                c += 1
            r += 1


    # Maybe use for i in range(self.row) instead of for l in self.grid
    def find_br(self, player, mixing=False, beliefs=None):
        """ Finds all the best responses of the specified player. This function only supports 
            the scenario where one player uses a mixed strategy and the other player plays a pure strategy.
            br stands for best responses and opm stands for one player mixing. Later we will have to make a function for both players mixing (bpm?)

            Keyword Arguments:
            player : (1 or 2) it specifies the number of the player that we are going to analyze 
            mixing : (boolean) 

            Returns:
            A List containing the coordinates of the best strategies for the specifies player.
        """
        if (player != 1) and (player != 2):
            raise ValueError("player must be an int with the value of 1 or 2")
        if not mixing:
            if player == 1:
                for i in range(self.columns):
                    br_coordinates = best = None
                    counter = 0
                    multiple_br_values = []
                    for row in self.grid:
                        current_value = row[i][player-1]
                        # in x, y format (columns, row)
                        current_value_coordinates = (i, counter)
                        if best is None or current_value > best:
                            best = current_value
                            br_coordinates = current_value_coordinates
                        elif best == current_value:
                            if current_value_coordinates not in multiple_br_values:
                                multiple_br_values.append(
                                    current_value_coordinates)
                        counter += 1
                    # we should have the highest value in column i for player 1 in the variable best
                    # and the coordinates for this cell in the variable br_coordinates (if there are multiple tuples with the same
                    # value then br_coordinates contains the position of the first tuple that was found with this value and the rest are in multiple_best_values)
                    if br_coordinates not in multiple_br_values:
                        multiple_br_values.append(br_coordinates)

                    for coordinates in multiple_br_values:
                        c = self.grid_pure_nash[coordinates[1]][coordinates[0]]
                        self.grid_pure_nash[coordinates[1]
                                            ][coordinates[0]] = ('H', c[1])
                    for value in multiple_br_values:
                        if value in self.p1_br:
                            continue
                        else:
                            self.p1_br.append(value)
                return self.p1_br
            elif player == 2:
                counter = 0
                for row in self.grid:
                    br_coordinates = best = None
                    multiple_br_values = []
                    for i in range(self.columns):
                        current_value = row[i][player-1]
                        # in x, y format (columns, row)
                        current_value_coordinates = (i, counter)
                        if best is None or current_value > best:
                            best = current_value
                            br_coordinates = current_value_coordinates
                        elif best == current_value:
                            if current_value_coordinates not in multiple_br_values:
                                multiple_br_values.append(
                                    current_value_coordinates)
                    counter += 1

                    if br_coordinates not in multiple_br_values:
                        multiple_br_values.append(br_coordinates)

                    for coordinates in multiple_br_values:
                        c = self.grid_pure_nash[coordinates[1]][coordinates[0]]
                        self.grid_pure_nash[coordinates[1]
                                            ][coordinates[0]] = (c[0], 'H')
                    for value in multiple_br_values:
                        if value in self.p2_br:
                            continue
                        else:
                            self.p2_br.append(value)
                return self.p2_br
        else:
            expected_payoffs = {}
            if player == 1:
                for i in range(self.rows):
                    result = 0
                    result_string = ''
                    for j in range(self.columns):
                        result += beliefs[j] * self.grid[i][j][player - 1]
                        result_string += f"({beliefs[j]} * {self.grid[i][j][player - 1]})"
                    # print(f"A{i + 1}: {result_string} = {result}")
                    key = f"A{i + 1}"
                    expected_payoffs[key] = result
                return expected_payoffs
            elif player == 2:
                for i in range(self.columns):
                    counter = 0
                    result = 0
                    result_string = ""
                    for row in self.grid:
                        p2_payoff = row[i][1]
                        b = beliefs[counter]
                        result += b * p2_payoff
                        result_string += f"({b} * {p2_payoff}) "
                        counter += 1
                    # print(f"B{i + 1} : {result_string} = {result}")
                    key = f"B{i + 1}"
                    expected_payoffs[key] = result
                return expected_payoffs

    def find_pure_nash_equi(self):
        player1 = self.find_br(player=1)
        player2 = self.find_br(player=2)
        self.nash_equilibria = [value for value in player1 if value in player2]
        return self.nash_equilibria

    def create_random_beliefs(self, mode='dirichlet'):
        if mode == 'dirichlet':
            # We can use the Dirichlet distribution https://en.wikipedia.org/wiki/Dirichlet_distribution
            p1_beliefs = np.random.dirichlet(np.ones(self.rows),size=1).tolist()[0] # we need the [0] because it is a list of lists
            p2_beliefs = np.random.dirichlet(np.ones(self.columns),size=1).tolist()[0]
        elif mode == 'sum':
            # Or we can create a random array of numbers, then get the sum and divide every number by the sum
            p1_rand_numbers = [random.random() for i in range(self.rows)]
            s = sum(p1_rand_numbers)
            p1_beliefs = [round(i/s, 3) for i in p1_rand_numbers]

            p2_rand_numbers = [random.random() for i in range(self.columns)]
            s = sum(p2_rand_numbers)
            p2_beliefs = [round(i/s, 3) for i in p2_rand_numbers]
        return [p1_beliefs, p2_beliefs]

    def print_pure_nash(self):
        columns = "\t"
        for i in range(self.columns):
            columns += f"    B{i + 1}\t\t\t"
        print(columns)
        r = 1
        for row in self.grid_pure_nash:
            row_string = f"A{r}\t"
            for c in row:
                new_value_x = str(c[0])
                new_value_y = str(c[1])

                while len(new_value_x) < 3:
                    new_value_x = " "+ new_value_x
                while len(new_value_y) < 3:
                    new_value_y = " "+ new_value_y
                    
                row_string += f"({new_value_x}, {new_value_y})\t\t"
            r += 1
            print(row_string)


    def ep_bpm(self, p1_beliefs, p2_beliefs):
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

    def get_indifference_probabilities(self):
        """Calculate the mixed strategy Nash equilibrium for a 2x2 game.
        
        If pure Nash equilibria exist (nash_equilibria is not empty), 
        we don't need to calculate mixed strategies, so return None.
        
        Returns:
            A list of two lists with the mixed strategy probabilities for each player,
            or None if pure Nash equilibria already exist.
        """
        if len(self.nash_equilibria) > 0:
            # If there are pure Nash equilibria, return None
            return None
            
        if len(self.nash_equilibria) == 0:
            # Starting with player 1. We need to find a strategy that makes player 2 indiferent
            # we can make a formula to find p
            #   p  | (?, x) | (?, z) |
            #      |--------|--------|
            #  1-p | (?, y) | (?, w) |
            # Now to make the expected payoff of player 2 the same regardless of the strategy that he plays
            #   p(x) + (1-p)(y) = p(z) + (1-p)(w)
            #       px + y - yp = pz + w - wp
            # px - py + wp - pz = w - y
            #  p(x - y + w - z) = w - y
            #                 p = (w - y) / (x - y + w - z)
            x = self.grid[0][0][1]
            y = self.grid[1][0][1]
            z = self.grid[0][1][1]
            w = self.grid[1][1][1]
            if (x - y + w - z) != 0:
                p = (w - y) / (x - y + w - z)
                if p < 0 or (1-p) < 0:
                    print("There are negative probabilities. One or more strategies may be dominated")
                    return []
            else:
                print("There is a problem (division by 0). One or more strategies may be dominated")
                return []
            p1_strategy = [p, 1-p]

            # We can make a similar case with player 2
            #           q       1-q
            #   p  | (x, ?) | (z, ?) |
            #      |--------|--------|
            #  1-p | (y, ?) | (w, ?) |
            # q(x) + (1-q)(z) = q(y) + (1-q)(w)
            #     qx + z - qz = qy + w - qw
            #                ...
            #               q = (w - z) / (x - z - y + w)
            x = self.grid[0][0][0]
            y = self.grid[1][0][0]
            z = self.grid[0][1][0]
            w = self.grid[1][1][0]
            if (x - y + w - z) != 0:
                q = (w - z) / (x - y + w - z)
                if q < 0 or (1-q) < 0:
                    print("There are negative probabilities. One or more strategies may be dominated")
                    return []
            else:
                print("There is a problem (division by 0). One or more strategies may be dominated")
                return []
            p2_strategy = [q, 1-q]

            return [p1_strategy, p2_strategy]