#  =============================================================================
#  Group Number: This	number	will	be	assign	to	you	in	canvas	in	the	grades	section
#
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
from normal_form.NormalForm import NormalForm

# First we need to ask the user if the mode is Random or Manual
# mode = input('Enter (R)andom or (M)anual payoffs enteries\n')
# rows = input('Enter the number of rows: ')
# columns = input('Enter the number of cols: ')
test_normal_form = NormalForm('R', rows=5, columns=2)
test_normal_form.add_payoffs()
test_normal_form.print_normal_form()
test_normal_form.print_strategies(player=1)
test_normal_form.print_payoffs(1)
test_normal_form.print_strategies(player=2)
test_normal_form.print_payoffs(2)

# Testing Pure strategies

print("Testing Pure strategies\n\n")

test_normal_form.find_br_opm(player=1, mixing=False)
test_normal_form.find_br_opm(player=2, mixing=False)
test_normal_form.print_normal_form()

# Testing Mixing strategies

# print("Testing Mix strategies\n\n")

# test_normal_form = NormalForm('R', rows=5, columns=2)
# test_normal_form.add_payoffs()
# test_normal_form.print_normal_form()
# test_normal_form.find_br_opm(player=1, mixing=True, beliefs=[1/6, 1/3, 1/2])
# test_normal_form.find_br_opm(player=2, mixing=True, beliefs=[1/6, 1/3, 1/2])