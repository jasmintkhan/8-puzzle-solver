# Jasmin Khan
# credit: TA assistance from Samarth Khanna, thank you! 

from collections import deque # using deque (double-ended queue) for BFS
import heapq # using priority queue for UCS and A*

def read_initial_state_from_file(filename):
    with open(filename, 'r') as file:
        return file.readline().strip()
    
def sum_top_row_goal_test(state):
    # extract the top row (positions 0, 1, and 2)
    top_row = state[:3]  # top row as a string
    # replace blank tile (_) with 0 and convert the row to integers
    top_row_numbers = [int(num) if num != '_' else 0 for num in top_row]
    # check if the sum equals 11
    return sum(top_row_numbers) == 11

# generate neighbors by moving the blank tile    
def get_neighbors(state):
    neighbors = []
    state_list = list(state)  # convert the state into a list of char
    blank_index = state_list.index('_')  # find the index of the blank/empty space
    row, col = divmod(blank_index, 3)  # convert index to 2D row and column

    # moves for the blank tile
    moves = {
        "U": (-1, 0),  # up
        "D": (1, 0),   # down
        "L": (0, -1),  # left
        "R": (0, 1)    # right
    }

    # map the direction based on the numbered tile's move, not the blank's move
    flip_direction = {
        "U": "D",  # blank moves up, so the tile below moves down
        "D": "U",  # blank moves down, so the tile above moves up
        "L": "R",  # blank moves left, so the tile to the right moves left
        "R": "L"   # blank moves right, so the tile to the left moves right
    }

    # try each move direction and check if it's valid (within bounds)
    for direction, (row_change, col_change) in moves.items():
        new_row, new_col = row + row_change, col + col_change
        
        # Check if the new position is within grid
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank_index = new_row * 3 + new_col  # convert back to 1D index
            new_state_list = state_list[:]  # create a copy of the state list (IMPORTANT!)
            
            # swap the blank tile with the target tile
            new_state_list[blank_index], new_state_list[new_blank_index] = new_state_list[new_blank_index], new_state_list[blank_index]
            
            # add the new state and the flipped move (numbered tile's direction)
            new_state_str = ''.join(new_state_list)
            #print(f"Generated new state from move {flip_direction[direction]}:")
            #print(format_state_as_grid(new_state_str))
            neighbors.append((f"{new_state_list[blank_index]}{flip_direction[direction]}", new_state_str))
    
    return neighbors

# DFS implementation to search for a solution path
def dfs(start_state):
    # stack to keep track of the path we are currently exploring
    stack = [(start_state, [])]  
    visited = set()  # avoid revisiting
    node_expansions = 0  # track the number of node expansions
    count = 0  # count for debugging
    
    while stack:
        current_state, path = stack.pop()  # LIFO behavior for DFS
        #print(f"Exploring #{count} state:\n{format_state_as_grid(current_state)}\n")
        count += 1

        # check if the goal is met (sum of the top row equals 11)
        if sum_top_row_goal_test(current_state):
            #print(f"Goal reached! Number of node expansions: {node_expansions}")
            return path, node_expansions  # return the solution path and node expansions

        # mark this state as visited
        if current_state not in visited:
            visited.add(current_state)
            node_expansions += 1  # increment the number of node expansions
            #print(f"Visited states: {visited}")

            # get possible moves (neighbors) and add them to the stack
            for move, new_state in get_neighbors(current_state):
                if new_state not in visited:
                    #print(f"Adding state to stack (from move {move}):\n{format_state_as_grid(new_state)}\n")
                    stack.append((new_state, path + [move]))  
    
    return None, node_expansions  # if no solution is found

# BFS implementation to search for a solution path
def bfs(start_state):
    # queue to keep track of the path we are currently exploring
    queue = deque([(start_state, [])])  # each element in queue is (current_state, path_to_this_state)
    visited = set()  # avoid revisiting
    node_expansions = 0  # track the number of node expansions
    
    while queue:
        current_state, path = queue.popleft()  # FIFO behavior for BFS
        
        # check if we reached the goal
        if sum_top_row_goal_test(current_state):
            return path, node_expansions  # return the solution path
        
        # mark this state as visited
        visited.add(current_state)
        node_expansions += 1  # Increment node expansions
        
        # get possible moves (neighbors) and add them to the queue
        for move, new_state in get_neighbors(current_state):
            if new_state not in visited:
                queue.append((new_state, path + [move]))
    
    return None, node_expansions  # if no solution is found

# UCS implementation to search for a solution path
def ucs(start_state):
    # priority queue to keep track of (cumulative_cost, current_state, path_to_this_state)
    pq = [(0, start_state, [])]  # start with cost 0 and an empty path
    visited = set()  # avoid revisiting
    node_expansions = 0  # track the number of node expansions
    
    while pq:
        cumulative_cost, current_state, path = heapq.heappop(pq)  # pop the least-cost node
        
        # check if we reached the goal
        if sum_top_row_goal_test(current_state):
            return path, node_expansions  # Return the solution path
        
        # mark this state as visited
        if current_state not in visited:
            visited.add(current_state)
            node_expansions += 1  # Increment node expansions
            
            # get possible moves (neighbors) and add them to the priority queue
            for move, new_state in get_neighbors(current_state):
                if new_state not in visited:
                    # each move has a cost of 1, so we add 1 to the cumulative cost
                    heapq.heappush(pq, (cumulative_cost + 1, new_state, path + [move]))
    
    return None, node_expansions  # if no solution is found

# calculate manhattan distance (using ideal position for sum of top row)
def manhattan_distance(state):
    distance = 0
    state_list = list(state)
    for i, tile in enumerate(state_list):
        if tile != "_":
            goal_pos = (int(tile) - 1) % 9  # the "ideal" position is based on the number itself (1 -> 0th position, 2 -> 1st position, etc.)
            curr_row, curr_col = divmod(i, 3)
            goal_row, goal_col = divmod(goal_pos, 3)
            distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance

# a* search implementation with customizable heuristic
def a_star(start_state, heuristic_func):
    # priority queue to keep track of (cost, current_state, path_to_this_state)
    pq = [(heuristic_func(start_state), 0, start_state, [])]  # (f(n), g(n), current_state, path)
    visited = set()
    node_expansions = 0  # track the number of node expansions
    
    while pq:
        f_cost, g_cost, current_state, path = heapq.heappop(pq)  # pop the least-cost node
        
        # check if we reached the goal
        if sum_top_row_goal_test(current_state):
            return path, node_expansions
        
        # mark this state as visited
        if current_state not in visited:
            visited.add(current_state)
            node_expansions += 1
            
            # get possible moves (neighbors) and add them to the priority queue
            for move, new_state in get_neighbors(current_state):
                if new_state not in visited:
                    new_g_cost = g_cost + 1  # Each move has a cost of 1
                    new_f_cost = new_g_cost + heuristic_func(new_state)
                    heapq.heappush(pq, (new_f_cost, new_g_cost, new_state, path + [move]))
    
    return None, node_expansions  # if no solution is found

# calculate euclidean distance (using ideal position for sum of top row)
def euclidean_distance(state):
    distance = 0
    state_list = list(state)
    for i, tile in enumerate(state_list):
        if tile != "_":
            goal_pos = goal_pos = (int(tile) - 1) % 9  # the "ideal" position is based on the number itself
            curr_row, curr_col = divmod(i, 3)
            goal_row, goal_col = divmod(goal_pos, 3)
            distance += ((curr_row - goal_row)**2 + (curr_col - goal_col)**2) ** 0.5  # Euclidean distance
    return distance

# format the state as a 3x3 grid
def format_state_as_grid(state):
    return '\n'.join([state[i:i+3] for i in range(0, len(state), 3)])

# main function
if __name__ == "__main__":
    # read the initial state from input.txt
    start_state = read_initial_state_from_file('input.txt').replace(",", "")  # convert from input format to raw string

    solution, expansion = dfs(start_state)
    print("The solution of Q2.1.a is:")
    if solution :
        print(','.join(solution))  # print the actual solution path
        #print(f"node expansions: {expansion}")
    else:
        print("No solution found.")

    print()
    solution, expansion = bfs(start_state)
    print("The solution of Q2.1.b is:")
    if solution:
        print(','.join(solution))  # print the actual solution path
        #print(f"node expansions: {expansion}")
    else:
        print("No solution found.")

    print()
    solution, expansion = ucs(start_state)
    print("The solution of Q2.1.c is:")
    if solution:
        print(','.join(solution))  # print the actual solution path
        #print(f"node expansions: {expansion}")
    else:
        print("No solution found.")

    print()
    solution, expansion = a_star(start_state, manhattan_distance)
    print("The solution of Q2.1.d is:")
    if solution:
        print(','.join(solution))  # print the actual solution path
        #print(f"node expansions: {expansion}")
    else:
        print("No solution found.")

    print()
    solution, expansion = a_star(start_state, euclidean_distance)
    print("The solution of Q2.1.e is:")
    if solution:
        print(','.join(solution))  # print the actual solution path
        #print(f"node expansions: {expansion}")
    else:
        print("No solution found.")