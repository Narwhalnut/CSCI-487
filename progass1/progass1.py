from boardstate import BoardState

# Initialize State
print("INITIAL")
initial = BoardState([1,2,3,0,4,5,7,8,6], 0)
# initial = BoardState([1,2,3,4,0,5,7,8,6], 0)
initial.EstimateTotalCost()
initial.Print()
print("CHILDREN")
children = initial.GetChildren()
for c in children:
    c.Print()

def AStar(root):
    step = 1
    keep_going = True
    path = []
    while (keep_going):
        print("\n######## A* SEARCH - STEP " + str(step) + " ########")
        user_response = input("PRESS ENTER")
        # Start at the root
        # Find the cheapest (estimated) path to a leaf leaf
        path = root.GetLowestCostPath([])
        # Expand it
        sentry = path[-1]
        children = sentry.GetChildren()
        sentry.Print()
        # print("EXPANDING INTO:")
        # Check if any of the expansions are the solution
        solution = None
        for c in children:
            # c.Print()
            if c.IsSolved():
                solution = c
        step = step + 1
        # If a solution was found, append it to the path and return.
        if solution != None:
            path.append(solution)
            keep_going = False
    return path

def BreadthFirst(sentry):
    pass

solution_path = AStar(initial);
print("######## SEARCH PATH FOUND ########")
for b in solution_path:
    b.Print()