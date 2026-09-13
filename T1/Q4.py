# read in input
# people
people = int(input())

# budget
budget = int(input())

# calculate money needed for those people, 30*pp
total = people * 30

# result = budget - total
result = budget - total

# output, if affordable, print remaining; else print need
if result >= 0:
    print("Remaining:", result)
else:
    print("Need:", -result)