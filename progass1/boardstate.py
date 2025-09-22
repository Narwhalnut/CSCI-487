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
        
        self.cheapest_possible_child = None
        
        self.children = []
        # Check if we are solved.
        self.solved = False
    
    def GetCheapestPossibleChild(self):
        # Get the cheapest child in this tree
        
        # If we have no children, use ourself
        if self.IsLeaf():
            return self
        # If the last found value is still valid, use it.
        if self.cheapest_possible_child != None and self.cheapest_possible_child.IsLeaf():
            return self.cheapest_possible_child
        
        # Search each child for the cheapest
        self.cheapest_possible_child = None
        for c in self.children:
            current_node = c.GetCheapestPossibleChild()
            if (self.cheapest_possible_child == None or current_node.estimated_total_cost < self.cheapest_possible_child.estimated_total_cost):
                self.cheapest_possible_child = current_node
        return self.cheapest_possible_child
    
    def IsSolved(self):
        # Getter
        return self.solved
        
    def GetChildren(self, closed_list):
        # Returns all children. Expands if not expanded already.
        if not self.children:
            self.children = self.Expand()
        return self.children
    
    def IsLeaf(self):
        # Checks if this node has been expanded yet.
        if not self.children:
            return True
        return False
    
    def EstimateTotalCost(self):
        # Estimate the total cost of this state based on the preceeding cost.
        cost = 0
        i = 0
        for tile_value in self.array:
            i = i + 1
            # If this tile is misplaced, that is an additional cost.
            if i == 9:
                # Don't care. This spot is supposed to be empty.
                pass
            elif i != tile_value:
                cost = cost + 1
        # Update "solved"
        self.solved = (cost == 0)
        # Update cost
        self.estimated_total_cost = cost + self.preceeding_real_cost
    
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