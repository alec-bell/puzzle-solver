import sys
import csv
import json
from copy import copy, deepcopy

def pretty_print(solution):
    for row in solution["img"]:
        for col in row:
            if col == -1:
                print(' ', end=' ')
            else:
                print(col, end=' ')
        print()

def bfs(state):
    queue = [state]
    while len(queue) > 0:
        current_state = queue.pop(0)
        if is_goal(current_state):
            return current_state
        queue.extend(successors(current_state))
    print("No solution")
    return None

def dfs(state):
    if is_goal(state):
        return state
    for successor in successors(state):
        result = dfs(successor)
        if result != None:
            return result
    return None

def successors(current_state):
    img = current_state["img"]
    piece = None
    for some_piece in current_state["pieces"]:
        if some_piece["count"] > 0:
            piece = some_piece
            break
    if piece is None:
        return []
    piece["count"] -= 1

    successors = []
    for rotation in get_rotations(piece):
        shape = rotation["shape"]
        for i in range(len(img) - len(shape) + 1):
            for j in range(len(img[0]) - len(shape[0]) + 1):
                valid_placement = True
                for k in range(len(shape)):
                    for l in range(len(shape[0])):
                        valid_placement = (shape[k][l] == 1 and img[i+k][j+l] == 0) or shape[k][l] == 0
                        if not valid_placement:
                            break
                    if not valid_placement:
                        break
                if valid_placement:
                    successor = deepcopy(current_state)
                    for k in range(len(shape)):
                        for l in range(len(shape[0])):
                            if (shape[k][l] == 1):
                                successor["img"][i+k][j+l] = rotation["id"]
                    successors.append(successor)
    return successors

def get_rotations(piece):
    rotations = [piece]
    for i in range(0, 4):
        rotation = rotations[i].copy()
        rotation["shape"] = rotate(rotation["shape"])
        rotations.append(rotation)
    return rotations

def rotate(mat):
    return list(zip(*mat[::-1]))

def is_goal(state):
    for piece in state["pieces"]:
        if piece["count"] > 0:
            return False
    return True

img_file_path = "images/2.csv"
comb_file_path = "combinations/2.json"

# Load image
with open(img_file_path) as f:
    reader = csv.reader(f)
    img = [list(map(int, rec)) for rec in reader]

# Load pieces
with open(comb_file_path) as f:
    pieces = json.loads(f.read())

state = {"img": img, "pieces": pieces}
solution = dfs(state)

pretty_print(solution)