import copy
HIGH = 32

class BoardState:
    # Represents an individual node in the search tree.
    # Can branch into each possible new state.
    # Print the board state.

    def __init__(self, tile_values, parent = None):
        # Constructor. Pass in the values of each tile and current cost.
        self.array = tile_values
        self.parent = parent
        if parent != None:
            self.preceeding_real_cost = parent.preceeding_real_cost + 1
        else:
            self.preceeding_real_cost = 0
        self.estimated_total_cost = -1
        self.is_closed = False
        
        self.cheapest_possible_child = None
        
        self.children = []
        self.solved = False
    
    def GetAllLeavesAtDepth(self, depth):
        # Get every child at the depth specified
        
        # This node is at the specified depth
        if depth == 0:
            return [self]
        
        # There are no nodes beneath me
        if self.IsLeaf():
            return []
        
        # Ask all this node's children for their leaves
        leaves = []
        for c in self.GetChildren():
            leaves_of_children = c.GetAllLeavesAtDepth(depth - 1)
            for l in leaves_of_children:
                leaves.append(l)
        return leaves
    
    def GetCheapestPossibleChild(self):
        # Get the cheapest child in this tree
        
        # If we have no children, use ourself
        if self.IsLeaf():
            return self
        # If the last found value is still valid, use it.
        if self.cheapest_possible_child != None and self.cheapest_possible_child.IsLeaf() and self.cheapest_possible_child.is_closed == False:
            return self.cheapest_possible_child
        
        # Otherwise, search each child for the cheapest
        self.cheapest_possible_child = None
        for c in self.children:
            current_node = c.GetCheapestPossibleChild()
            if (self.cheapest_possible_child == None or current_node.estimated_total_cost < self.cheapest_possible_child.estimated_total_cost):
                self.cheapest_possible_child = current_node
        return self.cheapest_possible_child
    
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
    
    def EstimateTotalCost(self):
        # This node is closed. Do not select it
        if self.is_closed:
            self.estimated_total_cost = HIGH
            return
    
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
            b = BoardState(copy.deepcopy(self.array), self)
            b.Swap(empty_slot_index,empty_slot_index-3)
            branches.append(b)
        # East Swap Branch
        if empty_slot_coords[0] < 2:
            b = BoardState(copy.deepcopy(self.array), self)
            b.Swap(empty_slot_index,empty_slot_index+1)
            branches.append(b)
        # South Swap Brach
        if empty_slot_coords[1] < 2:
            b = BoardState(copy.deepcopy(self.array), self)
            b.Swap(empty_slot_index,empty_slot_index+3)
            branches.append(b)
        # West Swap Branch
        if empty_slot_coords[0] > 0:
            b = BoardState(copy.deepcopy(self.array), self)
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
    
    def GetPath(self):
        # Returns the path of nodes to get to this object
        if self.parent == None:
            return []
        path = self.parent.GetPath()
        path.append(self)
        return path
    
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
        # print("    estimated total cost..." + str(self.estimated_total_cost))