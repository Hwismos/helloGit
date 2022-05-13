# human-based algorithm and A* algorithm for sliding puzzle game
# by Alan Huang and Nishant Nayak
# import matplotlib.pyplot as plt
# import numpy as np
import random
import sys
import argparse

FLAG = 'HUMAN'
parser = argparse.ArgumentParser()
parser.add_argument("--astar", help="perform A* search", action="store_true")
args = parser.parse_args()
if args.astar:
    FLAG = 'A_STAR'


# node class
class Node:
  def __init__(self, board, previous, heuristic, depth):
    self.board = board
    self.previous = previous
    self.heuristic = heuristic
    self.depth = depth # depth is 0 for best first search/greedy

  def __lt__(self, other):
    return True

  def generate_children(self):
    for i in range(n):
      for j in range(n):
        if self.board[i][j] == 0:
          x, y = i, j
    val_list = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]
    children = []
    for child in val_list:
      if child[0] >=0 and child [0] < n and child[1] >= 0 and child[1] < n:
        child_board = [row[:] for row in self.board]
        child_board[x][y] = child_board[child[0]][child[1]]
        child_board[child[0]][child[1]] = 0
        child_node = Node(child_board, self, node_manhattan(child_board), self.depth + 1)
        children.append(child_node)
    return children

# helper functions
def create_random_board(n, solvable = True):
  board = [[0 for i in range(n)] for j in range(n)]
  s = list(set([i for i in range(n * n)]))
  for i in range(n):
    for j in range(n):
      item = random.sample(s, 1)
      board[i][j] = item[0]
      s.remove(item[0])
  if solvable:
    if not isSolvable(board):
      if board[2][1] != 0 and board[2][2] != 0:
        temp = board[2][1]
        board[2][1] = board[2][2]
        board[2][2] = temp
      else:
        temp = board[0][0]
        board[0][0] = board[0][1]
        board[0][1] = temp
  return board

def plain_print(b):
  for i in b:
    for j in i:
      print(j, end = " ")
    print()

import heapq as pq

def node_manhattan(board):
  sum = 0
  n = len(board)
  for i in range(n):
    for j in range(n):
      x = int((board[i][j] - 1)/n) # row number
      y = int((board[i][j] - 1) % n) # col num
      if board[i][j] == 0:
        continue
      sum += abs(x-i) + abs(y - j)
      # changed return to 0 for BFS, sum for A*
  return sum

def manhattan(board, goal_nums):
  sum = 0
  count = 0
  for i in range(n):
    for j in range(n):
      if board[i][j] in goal_nums:
        x = int((board[i][j] - 1)/n) # row number
        y = int((board[i][j] - 1) % n) # col num
        sum += abs(x-i) + abs(y - j)
  return sum

def to_tuple(board):
  lst = []
  for i in range(n):
    for j in range(n):
      lst.append(board[i][j])
  return tuple(lst)

def isGoal(board, goal_nums):
  count = 0
  for i in range(n):
    for j in range(n):
      count += 1
      if count in goal_nums and board[i][j] != count:
        return False
  return True

def isSolvable(board):
  n = len(board)
  lst = []
  blank_on_even = False
  for i in range(n):
    for j in range(n):
      if board[i][j] != 0:
        lst.append(board[i][j])
      else:
        if i % 2 == 0:
          blank_on_even = True
  inversions = 0

  for i in range(len(lst)):
    for j in range(i + 1, len(lst)):
      if lst[i] > lst[j]:
        inversions += 1

  if n % 2 == 1:
    if inversions % 2 == 1:
      return False
    else:
      return True
  if (inversions % 2 == 0 and blank_on_even) or (inversions % 2 == 1 and not blank_on_even):
    return False

  return True

# solver
h = [] 
visited = set()
n = 4

board = create_random_board(n)
while not isSolvable(board):
  board = create_random_board(n)

goal_states = []
count = 1

def in_order_goal_states(n):
  goal_states = []
  c = 1
  for i in range(n):
    for j in range(n):
      if i == n-1 and j == n-1:
        break
      goal_states.append(set([c]))
      if i > 0 or j > 0:
        goal_states[-1] = goal_states[-1].union(goal_states[-2])
      c += 1
  return goal_states

def row_col_goal_states(n):
  goal_states = []
  for layer in range(n-2):
    for i in range(n - layer):
      goal_states.append(set([n * layer + i + 1]))
      if len(goal_states) > 1:
        goal_states[-1] = goal_states[-1].union(goal_states[-2])
    for i in range(n - layer - 1):
      goal_states.append(set([n+1 + i * (n)]))
      goal_states[-1] = goal_states[-1].union(goal_states[-2])
  goal_states.append(set(range(1,n*n)))
  return goal_states

if FLAG == 'A_STAR':
  goal_states = row_col_goal_states(n)
  goal_states = [goal_states[-1]]
elif FLAG == 'HUMAN':
  goal_states = row_col_goal_states(n)

h_scale_factor = 3
curr_goal = 0
root = Node(board, None, manhattan(board, goal_states[curr_goal]), 0)
pq.heappush(h, (root.depth + h_scale_factor * root.heuristic, root))
f = open("solution.txt", "w")

def to_string(board):
  s = ""
  for i in board:
    for j in i:
      s += str(j) + " "
  return s

while len(h) > 0:
  count += 1
  node = pq.heappop(h)[1]

  if isGoal(node.board, goal_states[curr_goal]):
    print("reached goal", curr_goal, goal_states[curr_goal])
    plain_print(node.board)
    print()
    h = [] 
    curr_goal += 1

    # if we achieve final goal state, write to output file and terminate program
    if curr_goal == len(goal_states):
      temp = node
      boards = []
      while temp != None:
        boards.append(temp.board)
        temp = temp.previous
      boards.reverse()
      for i in boards:
        f.write(to_string(i))
        f.write("\n") 
      f.close()
      break

    root = Node(board, None, manhattan(board, goal_states[curr_goal]), 0)
    pq.heappush(h, (root.depth + h_scale_factor * root.heuristic, root))

  t = to_tuple(node.board)
  visited.add(t)
  children = node.generate_children()
  for child in children:
    t = to_tuple(child.board)
    if t in visited:
      continue
    pq.heappush(h,(child.depth + h_scale_factor * manhattan(child.board, goal_states[curr_goal]), child))

print("Reached the goal state and solved the sliding puzzle! Check out output.txt file to see",
      "the step-by-step process from the start state to goal state.")