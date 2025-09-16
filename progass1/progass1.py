from boardstate import BoardState

# Initialize State
    # Expand into all possible board states to move to
b = BoardState([1,2,3,0,4,5,7,8,6], 0)
b.Print()

print("POSSIBLE BRANCHES:")
branches = b.Expand()

for b_new in branches:
    b_new.Print()

# For each state...
    # Survey all possible states to move to
    # Take the cheapest
        # Expand all board states
        # Append all possible board states to leaf list