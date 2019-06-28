
class Node: 
    def __init__(self, x, y,  parent=None):
        self.parent = parent 
        self.x = x
        self.y = y

        self.g = 0
        self.h = 0
        self.f = 0

        self.cost = 1
        self.neighbours = [] 
    
    def __eq__(self,other):  # Overwrite operator == to compare nodes
        return self.x == other.x and self.y == other.y
    

def read_from_file(filename): # Helpfunction that reads from file and adds symbols into an array
    f = open(filename,"r")
    f1 = f.readlines()
    board = []
    boardline = []
    for line in f1:
        for i in range(0,len(line)-1):
            boardline.append(line[i])
        board.append(boardline)
        boardline = []
    
    return board
   
   
def print_board(board):   # Helpfunction to visualize the board
    print()
    for i in range(0,len(board)):
        for j in range(0, len(board[i])):
            print(board[i][j], end=" ")
        print()
    print()

  

def cost_to_goal(current_node, goal): # Helpfunction that returns h-value
    return abs(goal.x - current_node.x) + abs(goal.y - current_node.y)

def find_lowest_f_value(open_list): # Helpfunction that returns the node with the lowest f-value
    lowest_f = open_list[0]
    for node in open_list:
        if node.f < lowest_f.f:
            lowest_f = node
    return lowest_f


def cost_of_moving(board, node): # Helpfunction that returns cost of node
    if board[node.x][node.y] == 'w': 
        return 100
    elif board[node.x][node.y] == 'm':
        return 50
    elif board[node.x][node.y] == 'f':
        return 10
    elif board[node.x][node.y] == 'g':
        return 5
    else:
        return 1


def astar_algorithm(filename):      # A* algorithm to find shortest path
    
    # Initialize board
    board = read_from_file(filename) 
    
    
    # Find start and end indexes in board
    for i in range(0, len(board)): 
        for j in range(0, len(board[i])): 
            if board[i][j] == "A":
                start = (i,j)
            elif board[i][j] == "B": 
                end = (i,j)
    
    # Initialize open + closed lists and start + end nodes
    open_list = []
    closed_list = []

    end_node = Node(end[0], end[1])
    end_node.g = end_node.h = end_node.f = 0
    start_node = Node(start[0], start[1])
    start_node.g = 0
    start_node.h = start_node.f = cost_to_goal(start_node, end_node)

    # Append startnode to openlist
    open_list.append(start_node)

    while len(open_list) > 0:
        
        current_node = find_lowest_f_value(open_list) # Find next node to explore
        open_list.remove(current_node) # Remove node from openlist
        closed_list.append(current_node) # Add node to closed_list

        # If we have reached the end node, draw new board and return
        if current_node == end_node:
            
            while current_node != start_node:
                current_node = current_node.parent
                board[current_node.x][current_node.y] = "O" 
            

            board[current_node.x][current_node.y] = "A" 
            print_board(board)
            return
        
        # Add neighbours

        # Find right neighbour
        if (current_node.y + 1 < len(board[0])) and (board[current_node.x][current_node.y+1] != '#'): # Check if in range and not obsticale
            right_nb = Node(current_node.x, current_node.y+1) # Create new node for neighbour

            right_nb.h = cost_to_goal(right_nb, end_node)     # Calculate heuristic value
            right_nb.cost = cost_of_moving(board, right_nb)   # Calculate cost for node

            if right_nb not in open_list:
                current_node.neighbours.append(right_nb)
                

        # Find left neighbour
        if (current_node.y-1 >= 0) and (board[current_node.x][current_node.y-1] != '#'): # Check if in range and not obsticale
            left_nb = Node(current_node.x, current_node.y-1) # Create new node for neighbour

            left_nb.h = cost_to_goal(left_nb, end_node)      # Calculate heuristic value
            left_nb.cost = cost_of_moving(board, left_nb)    # Calculate cost for node

            if left_nb not in open_list:
                current_node.neighbours.append(left_nb)

        #Find neighbour above
        if (current_node.x-1 >= 0) and (board[current_node.x-1][current_node.y] != '#'): # Check if in range and not obsticale
            above_nb = Node(current_node.x-1, current_node.y) # Create new node for neighbour

            above_nb.h = cost_to_goal(above_nb, end_node)     # Calculate heuristic value
            above_nb.cost = cost_of_moving(board,above_nb)    # Calculate cost for node

            if above_nb not in open_list:
                current_node.neighbours.append(above_nb)
        
        # Find neighbour below
        if (current_node.x+1 < len(board)) and (board[current_node.x+1][current_node.y] != '#'): # Check if in range and not obsticale
            below_nb = Node(current_node.x+1, current_node.y) # Create new node for neighbour
            
            below_nb.h = cost_to_goal(below_nb, end_node)     # Calculate heuristic value
            below_nb.cost = cost_of_moving(board, below_nb)   # Calculate cost for node

            if below_nb not in open_list:                    
                current_node.neighbours.append(below_nb)

        for node in current_node.neighbours:    # Calculate f-value for new nodes to be added
            if node not in closed_list:
                open_list.append(node)
                if node.g < (current_node.g + node.cost):
                    node.g = (current_node.g + node.cost)
                    node.parent = current_node
                    node.f = node.g + node.h



        

    

astar_algorithm("board-2-2.txt")
