# read input and convert the raw data to integers
people = int(input())
budget = int(input())

# calculate the final cost
# exactly 4 people get the $100 lunch deal
if people == 4:
    cost = 100
else:
    cost = people * 30

# print the final cost
print(cost)

# check whether the budget is enough
# exactly enough money also counts as enough
if budget >= cost:
    print("Enough money")
else:
    print("Not enough money")