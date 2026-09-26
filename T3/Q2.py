# Start with the given dictionary
rooms = {1: 'hall', 3: 'lab', 5: 'garden'}

# Read how many room codes will be queried
n = int(input())

# Read and process n room codes
for _ in range(n):
    code = int(input())

    # Look up the room code in the dictionary
    # If the code is not a key, return 'UNKNOWN'
    print(rooms.get(code, 'UNKNOWN'))