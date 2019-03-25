import random 

class NormalForm():

    def __init__(self, mode, rows, columns, lower_limit=-99, upper_limit=99):
        """ Initialize a grid that represents the normal form of a game

            Keyword Arguments:

            mode: random or manual. If 'random' then we generate values in the range (lower_limit, upper_limit)
            rows: number of rows in the normal form grid (the number of strategies for player 2)
            columns: number of columsn in the normal for grid (the number of strategies for player 1)
            lower_limit: lower limit for the random values for payoffs if the mode is set to random
            upper_limit: upper limit for the random values for payoffs if the mode is set to random
        """
        self.rows = rows
        self.columns = columns
        self.mode = mode.lower() # except if the mode is not 'random' or 'manual'
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.grid = [[ (0,0) for i in range(self.columns)] for j in range(self.rows)] # a list of lists for the rows and columns in the normal form
        self.nash_equilibria = [] # a list of tuples that represent the x and y coordinates each nash equilibrium
        self.p1_br = [] # the set of best responses for player 1 
        self.p2_br = [] # the set of best responses for player 2 
        
    
    # We need to fix the format in this function. 
    def print_payoffs(self, player):
        payoffs = ""
        count = 0
        num_rows = 7
        if player == 1:
           for rows in self.grid:
                for col in rows:
                    if count == num_rows:
                       payoffs += str(col[0]) + "\n" 
                       count = 0
                    else:
                        payoffs += str(col[0]) + " "
                count += 1
        elif player == 2:
            for rows in self.grid:
                for col in rows:
                    if count == num_rows:
                        payoffs += str(col[1]) + "\n" 
                        count = 0
                    else:
                        payoffs += str(col[1]) + " "
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
            columns += f"B{i + 1}\t\t\t"
        print(columns)
        r = 1
        for row in self.grid:
            row_string = f"A{r}\t"
            for c in row:
                row_string += f"{c}\t\t"
            r += 1
            print(row_string)

    def add_payoffs(self):
        r = 0 # this is just a counter for displaying the cells in the normal form as A1, A2, ...
        for row in self.grid:
            c = 0
            for column in row:
                if self.mode == 'r':
                    p1 = random.randint(self.lower_limit, self.upper_limit)
                    p2 = random.randint(self.lower_limit, self.upper_limit)
                    self.grid[r][c] = (p1, p2)
                elif self.mode == 'm':
                    payoff = input(f"Enter payoff for ( A{r + 1}, B{c + 1} ) = ")
                    values = payoff.split(',')
                    self.grid[r][c] = (int(values[0]), int(values[1]))
                else:
                    raise ValueError
                c += 1
            r += 1

    # Maybe use for i in range(self.row) instead of for l in self.grid
    def find_br_opm(self, player, mixing=False, beliefs=None):
        """ Finds all the best responses of the specified player. This function only supports 
            the scenario where one player uses a mixed strategy and the other player plays a pure strategy.
            br stands for best responses and opm stands for one player mixing. Later we will have to make a function for both players mixing (bpm?)

            Keyword Arguments:
            player : (1 or 2) it specifies the number of the player that we are going to analyze 
            mixing : (boolean) 

            Returns:
            A List containing the coordinates of the best strategies for the specifies player.
        """
        if (player is not 1) and (player is not 2):
            raise ValueError("player must be an int with the value of 1 or 2")
        if not mixing:  
            if player is 1:
                for i in range(self.columns):
                    br_coordinates = best = None
                    counter = 0
                    multiple_br_values = []
                    for l in self.grid:
                        current_value = l[i][player-1]
                        current_value_coordinates = (i, counter) # in x, y format (columns, row)
                        if best is None or current_value > best:
                            best = current_value
                            br_coordinates = current_value_coordinates
                        elif best == current_value:
                            if current_value_coordinates not in multiple_br_values:
                                multiple_br_values.append(current_value_coordinates)

                        counter += 1
                    # we should have the highest value in column i for player 1 in the variable best
                    # and the coordinates for this cell in the variable br_coordinates (if there are multiple tuples with the same 
                    # value then br_coordinates contains the position of the first tuple that was found with this value and the rest are in multiple_best_values)
                    if br_coordinates not in multiple_br_values:
                        multiple_br_values.append(br_coordinates)

                    for coordinates in multiple_br_values:
                        c = self.grid[coordinates[1]][coordinates[0]]
                        self.grid[coordinates[1]][coordinates[0]] = ('H', c[1])

                    self.p1_br += multiple_br_values
                return self.p1_br
            elif player is 2:
                counter = 0
                for l in self.grid:
                    br_coordinates = best = None
                    multiple_br_values = []
                    for i in range(self.columns):
                        current_value = l[i][player-1]
                        current_value_coordinates = (i, counter) # in x, y format (columns, row)
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
                        c = self.grid[coordinates[1]][coordinates[0]]
                        self.grid[coordinates[1]][coordinates[0]] = (c[0], 'H')
                    self.p2_br += multiple_br_values
                return self.p2_br

        else:
            if player is 1:
                for l in self.grid:
                    result = 0
                    counter = 0
                    result_string = ""
                    for cell in l:
                        result += beliefs[counter] * cell[player-1] 
                        result_string += f"({beliefs[counter]} * {cell[player-1] })"
                        if counter != len(l)-1:
                            result_string += ' + '
                        counter += 1
                    print(f"A{counter + 1} : {result_string} = {result}")
                    return []
            elif player is 2:
                for i in range(self.columns):
                    counter = 0
                    result = 0
                    result_string = ""
                    for l in self.grid:
                        p2_payoff = l[i][1]
                        b = beliefs[counter]
                        result += b * p2_payoff
                        result_string += f"({b} * {p2_payoff}) "
                        counter += 1
                    print(f"B {i + 1} : {result_string} = {result}")


            return []

