# Start with the room list in the given order
rooms = ['hall', 'lab', 'store', 'garden']

# Read two positions from the user
a = int(input())
b = int(input())

# Swap the rooms at positions a and b
rooms[a], rooms[b] = rooms[b], rooms[a]

# Print all room names, one per line
for room in rooms:
    print(room)