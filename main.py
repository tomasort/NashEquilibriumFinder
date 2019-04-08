#  =============================================================================
#  Group Number: 30
#
# PROGRAMMER1: Tomas Ortega
#  PANTHER	ID1: 5677483
 
# PROGRAMMER2: Pablo Mueller
#  	PANTHER	ID2: 3283876
 
#  	CLASS: CAP4506	
#  	SECTION: U01
#  	SEMESTER: Spring 2019
#  	CLASSTIME: M/W	6:25-7:45 PM
 
#  	Project: This program will alow the user to find nash equilibriums and calculate expected payoffs for each player. 
#  	DUE: Sunday, April	7,	2019 at midnight.							
 
#  	CERTIFICATION: I certify	that	this	work	is	my own	and	that none	of it is the work of any other	person.
#  =============================================================================

import random

from normal_form.NormalForm import NormalForm

# First we need to ask the user if the mode is Random or Manual
# mode = input('Enter (R)andom or (M)anual payoffs enteries\n')
# rows rows input('Encolser the number of rows:rows')
# columcolss = input('Enter the number of cols: ')

def from_list_to_beliefs(lst):
  belief = "("
  for i in range(len(lst)):
    belief += f"{lst[i]}"
    if i == len(lst) - 1:
      belief += ")"
    else:
      belief += ", "
  return belief

while True:
  i = input("Enter (R)andom or (M)anual payoffs enteries:\n")
  if i == 'R' or i == 'M' or i == 'r' or i == 'm':
    i = i.lower()
    break
  print('Invalid selection')
  
while True:
  rows = input("Enter the number of rows (min 1, max 9):\n")
  rows = int(rows)
  if rows >= 1 and rows <= 9: 
    break
  print('Invalid selection')

while True:
  cols = input("Enter the number of columns (min 1, max 9):\n")
  cols = int(cols)
  if cols >= 1 and cols <= 9: 
    break
  print('Invalid Selection')

test_normal_form = NormalForm(i, rows=rows, columns=cols)
test_normal_form.add_payoffs()
print('\n')
print('\n------------------------------------')
print('Player: Player1\'s strategies')
print('\n------------------------------------')
test_normal_form.print_strategies(player=1)
print('\n------------------------------------')
print('Player: Player1\'s payoffs')
print('------------------------------------')
test_normal_form.print_payoffs(1) # fix formatting
print('\n------------------------------------')
print('Player: Player2\'s strategies')
print('\n------------------------------------')
test_normal_form.print_strategies(player=2)
print('\n------------------------------------')
print('Player: Player2\'s payoffs')
print('\n------------------------------------')
test_normal_form.print_payoffs(2)

print("\n=======================================")
print("Display Normal Form")
print("=======================================")
test_normal_form.print_normal_form()

print("\n=======================================")
print("Nash Pure Equilibrium Locations")
print("=======================================")
nash_eq_coordinates = test_normal_form.find_pure_nash_equi()
test_normal_form.print_pure_nash()
coordinates = ""
for c in nash_eq_coordinates:
  coordinates += f"(A{c[1] + 1}, B{c[0] + 1})   "

if coordinates == "":
  coordinates = "None"
print(f"\nNash Pure Equilibrium(s): {coordinates}")

beliefs = test_normal_form.create_random_beliefs(mode='sum')
print('\n------------------------------------')
print('Player 1 Expected Payoffs with Player 2 Mixing')
print('------------------------------------')
p1_eps = test_normal_form.find_br(player=1, mixing=True, beliefs=beliefs[1])
br = None
for key, value in p1_eps.items():
    print(f"U({key}, {from_list_to_beliefs(beliefs[1])}) = {round(value, 3)}")
    if br == None:
        br = key
    else:
        if p1_eps[br] < value:
            br = key

print('\n------------------------------------')
print('Player 1 Best Response with Player 2 Mixing')
print('------------------------------------')
br = "{" + str(br) + "}"
print(f"BR({from_list_to_beliefs(beliefs[1])}) = {br}")

print('\n------------------------------------')
print('Player 2 Expected Payoffs with Player 1 Mixing')
print('------------------------------------')
p2_eps = test_normal_form.find_br(player=2, mixing=True, beliefs=beliefs[0])
br = None
for key, value in p2_eps.items():
    print(f"U({key}, {from_list_to_beliefs(beliefs[0])}) = {round(value, 3)}")
    if br == None:
        br = key
    else:
        if p2_eps[br] < value:
            br = key

print('\n------------------------------------')
print('Player 2 Best Response with Player 1 Mixing')
print('------------------------------------')
br = "{" + str(br) + "}"
print(f"BR({from_list_to_beliefs(beliefs[1])}) = {br}")

print('\n------------------------------------')
print('Player 1 & 2 Expected Payoffs with both Players Mixing')
print('------------------------------------')
eps = test_normal_form.ep_bpm(p1_beliefs=beliefs[1], p2_beliefs=beliefs[0])
print(f"Player 1 -> U({from_list_to_beliefs(beliefs[0])}, {from_list_to_beliefs(beliefs[1])}) = {round(eps[0], 3)}")
print(f"Player 2 -> U({from_list_to_beliefs(beliefs[0])}, {from_list_to_beliefs(beliefs[1])}) = {round(eps[1], 3)}")

if rows == 2 and cols == 2:
    print('------------------------------------')
    print('Player 1 & 2 Indifferent Mix Probabilities')
    print('------------------------------------')
    if len(nash_eq_coordinates) == 0:
        # we need to find the mixing strategies for the nash eq 
        probabilities = test_normal_form.get_indifference_probabilities()
        for i in range(len(probabilities[0])):
            print(f"Player 1 probability of strategies (A{i + 1}) = {probabilities[0][i]}")

        for i in range(len(probabilities[1])):
            print(f"Player 2 probability of strategies (B{i + 1}) = {probabilities[1][i]}")
    else:
        print("Normal Form has Pure Strategy Equilibrium")

print("\n\n\n")

# Testing Pure strategies

# print("Testing Pure strategies\n\n")

# test_normal_form.find_br(player=1, mixing=False)
# test_normal_form.find_br(player=2, mixing=False)
# test_normal_form.print_normal_form()

# Testing Mixing strategies

# print("Testing Mix strategies\n\n")

# test_normal_form = NormalForm(i, rows=rows, columns=cols)
# test_normal_form.add_payoffs()
# test_normal_form.print_normal_form()
# test_normal_form.find_br(player=1, mixing=True, beliefs=[1/6, 1/3, 1/2])
# test_normal_form.find_br(player=2, mixing=True, beliefs=[1/6, 1/3, 1/2])


# print("Testing Nash eq")
# test_normal_form.find_br(player=1, mixing=False)
# test_normal_form.find_br(player=2, mixing=False)
# test_normal_form.print_pure_nash()
# x = test_normal_form.find_pure_nash_equi()
# print(x)

# print("Testing both Players Mixing")
# test_normal_form = NormalForm(i, rows=rows, columns=cols)
# test_normal_form.add_payoffs()
# test_normal_form.ep_bpm([1/6, 1/3, 1/2], [1/6, 1/3, 1/2])


# print("Testing Indiference")
# test_normal_form = NormalForm(i, rows=rows, columns=cols)
# test_normal_form.add_payoffs()
# x = test_normal_form.get_indifference_probabilities()
# test_normal_form.print_normal_form()
# print(x)
# test_normal_form.find_br(player=1, mixing=True, beliefs=x[1])
# test_normal_form.find_br(player=2, mixing=True, beliefs=x[0])
