from boardstate import BoardState
import random
import copy

random.seed("smeal")

def AStar(root):
    step = 1
    closed_list = []
    keep_going = True
    path = []
    while (keep_going):
        # Start at the root
        # Find the cheapest (estimated) child
        sentry = root.GetCheapestPossibleChild()
        cost = sentry.estimated_total_cost
        # Expand it
        children = sentry.GetChildren(closed_list)
        # sentry.Print()
        # Check for a solution
        solution = None
        for c in children:
            if c.IsSolved():
                solution = c
        step = step + 1
        # If a solution was found, append it to the path and return.
        if solution != None:
            print("######## A* SEARCH SUCCESS ########")
            print(str(cost) + " moves")
            keep_going = False
        else:
            # Always solvable in 31 possible moves. If above 31, give up.
            if cost > 31:
                print("######## A* SEARCH FAILED (>31 Moves) ########")
                path = []
                keep_going = False
            else:
                # Occassional User Feedback
                if step % 500000 == 0:
                    print("Searching... cost >= " + str(cost) + " moves")
    return path

def BreadthFirst(sentry):
    pass

# Initialize 3 States and try all searches
initial_array = [1,2,3,4,5,6,7,8,0]
initial_states = []
for i in range(3):
    random.shuffle(initial_array)
    initial = BoardState(copy.deepcopy(initial_array), 0)
    # initial = BoardState([5,1,3,0,2,6,4,7,8], 0) # Displays a perfect, followable test case
    # initial = BoardState([4,1,3,7,2,5,8,0,6], 0) # Displays a perfect, followable test case
    initial_states.append(initial)

for initial in initial_states:
    initial.EstimateTotalCost()
    print("\n######## INITIAL BOARD ########")
    initial.Print()
    solution_path = AStar(initial);
    if False:
        for b in solution_path:
            b.Print()