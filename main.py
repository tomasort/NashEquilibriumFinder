#  =============================================================================
#  Group	Number: This	number	will	be	assign	to	you	in	canvas	in	the	grades	section
# PROGRAMMER1: Tomas Ortega
#  PANTHER	ID1: 5677483
 
# PROGRAMMER2: Pablo Mueller
#  	PANTHER	ID2: Your	panther	ID
 
#  	CLASS: CAP4506	
#  	SECTION: U01
#  	SEMESTER: Spring 2019
#  	CLASSTIME: T/TH	6:25-7:45 PM
 
#  	Project: This program will alow the user to find nash equilibriums and calculate expected payoffs for each player. 
#  	DUE: Sunday, March	31,	2019 at midnight.							
 
#  	CERTIFICATION:	 I	certify	that	this	work	is	my	own	and	that
#  																															 none	of	it	is	the	work	of	any	other	person.
#  =============================================================================
import random 

class NormalForm():

    def __init__(self, mode, rows, columns, lower_limit=-99, upper_limit=99):
        self.rows = rows
        self.columns = columns
        self.mode = mode.lower()
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.nf = [[ (0,0) for i in range(self.columns)] for j in range(self.rows)]
    
    def print_payoffs(self, player):
        payoffs = ""
        if player == 1:
           for rows in self.nf:
                for col in rows:
                    payoffs += str(col[0]) + " "
        elif player == 2:
            for rows in self.nf:
                for col in rows:
                    payoffs += str(col[1]) + " "
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
        for row in self.nf:
            row_string = f"A{r}\t"
            for c in row:
                row_string += f"{c}\t\t"
            r += 1
            print(row_string)

    def add_payoffs(self):
        r = 0 # this is just a counter for displaying the cells in the normal form as A1, A2, ...
        for row in self.nf:
            c = 0
            for column in row:
                if self.mode == 'r':
                    p1 = random.randint(self.lower_limit, self.upper_limit)
                    p2 = random.randint(self.lower_limit, self.upper_limit)
                    self.nf[r][c] = (p1, p2)
                elif self.mode == 'm':
                    payoff = input(f"Enter payoff for ( A{r + 1}, B{c + 1} ) = ")
                    values = payoff.split(',')
                    self.nf[r][c] = (int(values[0]), int(values[1]))
                else:
                    raise ValueError
                c += 1
            r += 1



# First we need to ask the user if the mode is Random or Manual
mode = input('Enter (R)andom or (M)anual payoffs enteries\n')
rows = input('Enter the number of rows: ')
columns = input('Enter the number of cols: ')

test_normal_form = NormalForm(mode, int(rows), int(columns))
test_normal_form.add_payoffs()
test_normal_form.print_normal_form()
test_normal_form.print_strategies(player=1)
test_normal_form.print_payoffs(1)
test_normal_form.print_strategies(player=2)
test_normal_form.print_payoffs(2)