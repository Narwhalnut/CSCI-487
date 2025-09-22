import copy

class BoardState:
    # Represents an individual node in the search tree.
    # Can branch into each possible new state.
    # Print the board state.

    def __init__(self, tile_values, preceeding_real_cost):
        # Constructor. Pass in the values of each tile and current cost.
        self.array = tile_values
        self.preceeding_real_cost = preceeding_real_cost
        self.estimated_total_cost = -1
        
        self.children = []
        # Check if we are solved.
        self.solved = False
        
    def IsSolved(self):
        # Getter
        return self.solved
        
    def GetChildren(self):
        # Returns all children. Expands if not expanded already.
        if not self.children:
            self.children = self.Expand()
        return self.children
    
    def IsLeaf(self):
        # Checks if this node has been expanded yet.
        if not self.children:
            return True
        return False
        
    def GetLowestCostPath(self,preceeding_path):
        # Returns the lowest cost path to a leaf in the current tree (recursive).
        path = copy.deepcopy(preceeding_path)
        path.append(self)
        cheapest_path = None
        
        if self.IsLeaf():
            # If there are no children, this is the end of this path.
            cheapest_path = path
        else:
            # Check all children to find the cheapest (estimated) value.
            for c in self.children:
                current_node = c.GetLowestCostPath(path)
                if (cheapest_path == None or current_node[-1].estimated_total_cost < cheapest_path[-1].estimated_total_cost):
                    cheapest_path = current_node
                    current_cost = cheapest_path[-1].estimated_total_cost
        return cheapest_path
                
    
    def EstimateTotalCost(self):
        # Estimate the total cost of this state based on the preceeding cost.
        cost = self.preceeding_real_cost
        i = 0
        for tile_value in self.array:
            i = i + 1
            # If this tile is displaced, that is an additional cost.
            if i == 9:
                # Don't care. This spot is supposed to be empty.
                pass
            elif i != tile_value:
                cost = cost + 1
        # Update "solved"
        self.solved = (cost == self.preceeding_real_cost)
        # Update cost
        self.estimated_total_cost = cost
    
    def Expand(self):
        # Calculates 4 possible moves and returns them.
        
        # Start by finding the empty slot.
        empty_slot_coords = [0,0]
        empty_slot_index = 0
        i = 0
        for tile_value in self.array:
            if tile_value == 0:
                empty_slot_coords[0] = i % 3
                empty_slot_coords[1] = i // 3
                empty_slot_index = i
                break
            i = i + 1
        
        branches = []
        # For each possible adjacent swap for the empty index, create a branch.
        # North Swap Branch
        if empty_slot_coords[1] > 0:
            b = BoardState(copy.deepcopy(self.array), self.preceeding_real_cost+1)
            b.Swap(empty_slot_index,empty_slot_index-3)
            branches.append(b)
        # East Swap Branch
        if empty_slot_coords[0] < 2:
            b = BoardState(copy.deepcopy(self.array), self.preceeding_real_cost+1)
            b.Swap(empty_slot_index,empty_slot_index+1)
            branches.append(b)
        # South Swap Brach
        if empty_slot_coords[1] < 2:
            b = BoardState(copy.deepcopy(self.array), self.preceeding_real_cost+1)
            b.Swap(empty_slot_index,empty_slot_index+3)
            branches.append(b)
        # West Swap Branch
        if empty_slot_coords[0] > 0:
            b = BoardState(copy.deepcopy(self.array), self.preceeding_real_cost+1)
            b.Swap(empty_slot_index,empty_slot_index-1)
            branches.append(b)
        # Evaluate each branch when created
        for b in branches:
            b.EstimateTotalCost()
        # Return all newly created branches.
        return branches
    
    def Swap(self,index1,index2):
        # Swaps the values at the two given positions
        held = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = held
        # Be sure to update the cost
        self.EstimateTotalCost()
    
    def Print(self):
        # Print the board state in an easily human readable way
        i = 0
        for tile_value in self.array:
            ending = " "
            value = "_"
            # Newline every 3rd character
            if i == 2:
                ending = "\n"
            # Zero is empty. Do not display it.
            if tile_value != 0:
                value = str(tile_value)
            print(value, end=ending)
            i = (i + 1) % 3
        print("    estimated total cost..." + str(self.estimated_total_cost))