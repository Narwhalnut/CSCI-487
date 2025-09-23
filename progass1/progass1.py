from boardstate import BoardState
import random
import copy

EXPANSION_LIMIT = 100000
random.seed("smeal")

def main():
    # Initialize 3 Random States
    initial_array = [1,2,3,4,5,6,7,8,0]
    initial_states = []
    print("#### INITIAL BOARDS ####")
    for i in range(3):
        random.shuffle(initial_array)
        initial = BoardState(copy.deepcopy(initial_array))
        initial.EstimateTotalCost()
        initial_states.append(initial)
        initial.Print()
        print("------")
    # Searches each state using each method
    print("For each board, two search methods will be executed:")
    print("Breadth-First Search and A* Search.")
    for initial in initial_states:
        print("#### BREADTH-FIRST SEARCH BEGIN ####")
        initial.Print()
        input("PRESS ENTER")
        solution_path = BreadthFirst(initial);
        print("#### A* SEARCH BEGIN ####")
        initial.Print()
        input("PRESS ENTER")
        solution_path = AStar(initial);

def AStar(root):
    # Implements the A* search from a given root
    # Start at the root
    step = 0
    closed_list = []
    keep_going = True
    while (keep_going):
        # Find the cheapest (estimated) child
        sentry = root.GetCheapestPossibleChild()
        # If the selected node is in the closed list, ignore it.
        if sentry.array in closed_list:
            sentry.is_closed = True
            sentry.EstimateTotalCost()
            continue
        else:
            # Mark this node as being in the closed list.
            closed_list.append(sentry.array)
        # Expand it
        step = step + 1
        cost = sentry.estimated_total_cost
        children = sentry.GetChildren()
        # Check for a solution in the children
        solution = None
        for c in children:
            if c.IsSolved():
                solution = c
        # If a solution was found, append it to the path and return.
        if solution != None:
            print("#### A* SEARCH SUCCESS ####")
            path = solution.GetPath()
            for p in path:
                p.Print()
                print("------")
            print("A Path of " + str(cost) + " moves was found in " + str(step) + " expansions.")
            keep_going = False
        else:
            # Always solvable in 31 possible moves. If above 31, give up.
            if step >= EXPANSION_LIMIT:
                print("#### SEARCH FAILED ####")
                print("A path could not be found in the expansion limit (" + str(EXPANSION_LIMIT) + ").")
                print("It is unlikely that this configuration is solvable.")
                keep_going = False
            else:
                # Occassional User Feedback
                if step % 10000 == 0:
                    print("Searching... " + str(step) + " expansions.")

def BreadthFirst(root):
    # Implements the breadth first search from a given root
    # Start at the root
    step = 0
    depth = 0
    closed_list = []
    solution = None
    keep_going = True
    while (keep_going):
        # Try every node at the given depth
        for sentry in root.GetAllLeavesAtDepth(depth):
            if sentry.array in closed_list:
                # This node has been expanded before and was not solved. Do not expand.
                pass
            else:
                # Expand it
                children = sentry.GetChildren()
                closed_list.append(sentry.array)
                step = step + 1
                # Check for a solution in the children
                for c in children:
                    if c.IsSolved():
                        solution = c
                        break
        depth = depth + 1
        # If a solution was found, append it to the path and return.
        if solution != None:
            print("#### BREADTH-FIRST SEARCH SUCCESS ####")
            path = solution.GetPath()
            for p in path:
                p.Print()
                print("------")
            cost = solution.preceeding_real_cost
            print("A Path of " + str(cost) + " moves was found in " + str(step) + " expansions.")
            keep_going = False
        else:
            # Always solvable in 31 possible moves. If above 31, give up.
            if step >= EXPANSION_LIMIT:
                print("#### SEARCH FAILED ####")
                print("A path could not be found in the expansion limit (" + str(EXPANSION_LIMIT) + ").")
                print("It is unlikely that this configuration is solvable.")
                keep_going = False
            else:
                # Occassional User Feedback
                if depth > 10:
                    print("Searching... " + str(step) + " expansions.")

if __name__ == "__main__":
    main()