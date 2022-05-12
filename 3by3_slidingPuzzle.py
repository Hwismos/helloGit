from queue import PriorityQueue
import copy

board = [
    [8, 5, 7],
    [2, 3, 6],   #initial board state       # 초기 board
    [1, 4, 0],
]

board_solved = [
    [1, 2, 3],
    [4, 5, 6],  #goal board state           # 목표 board / 정렬된 상태
    [7, 8, 0],
]

count = 0   #represents node number         # node 수?
initial = copy.deepcopy(board)  #represents initial board state
board_previous = copy.deepcopy(board)  #represents board before going one move right/left/up/down
# 초기 board 상태와 previous board 상태를 저장

# board가 풀 수 있는지를 확인
# n X n이 아닐 때도 가능 → 다른 방법으로 구현해둠
def is_solvable():    #calculates number of inversions and returns whether board is solvable
    inversions = 0
    for i in range(1,9):
        x1, y1 = find(board, i)
        for j in range(i+1, 9):
            x2, y2 = find(board, j)
            if x2 - x1 == 0 and y2 - y1 < 0:
                inversions += 1
            elif x2 - x1 < 0:
                inversions += 1
    if inversions % 2 == 0:      #if number of inversions odd -> board not solvable
        return True
    else:
        return False


def backtrack(n1):   #determines the specific moves that led to the current state
    current = n1    # node가... node 사이의 거리 탐색       # node가 하나의 board       # 그래서 클래스로 node에 postion attribution을 준건가?
    g_score = 0     # g_socre이면 시작 노드부터의 거리
    solved = False
    if current == board_solved:     # 현재(current) board가 goal board면 해당 board 출력
        for x in current:
            print(x)
        print("\n")
    while current != came_from["previous_node0"]:       # came_from의 "previous node0" key에 해당하는 value가 아니면 loop를 돔
        if current == board_solved:     # 지금 board가 goal board면 solved flag에 True 저장
            solved = True
        for i in range(0,len(nodes.keys())):      #node number correlates to the node it came from
            if nodes["node%s" %i] == current:     #goes through all the nodes until it finds the previous node
                current = came_from["previous_node%s" %i]
                g_score += 1
                if solved:       #prints the steps when "current" equals the goal state
                    for x in current:
                        print(x)
                    print("\n")
                    if current == initial:  #stops backtracking when current equals initial board state
                        print(str(g_score) + " moves \n")
                if current == came_from["previous_node0"]:
                    return g_score   #number of backtracks = g score

                break


def distance():  #calculates manhattan distance         # 이건 그냥 휴리스틱 가중치 구하는 방법 중 Manhattan distance method 쓴 거임
    man = 0
    for i in range(1,9):
        x1, y1 = find(board, i)
        x2, y2 = find(board_solved, i)
        distance = abs(x2 - x1) + abs(y2 - y1)
        man += distance
    return man


def RLrestrict():   #if empty space is on far right/left of board, it will restrict the right/left move         # board에서 경계지역 넘어가지 않게 제한하는 함수
    global allow_r      # global 변수 썼네
    global allow_l
    allow_r = True
    allow_l = True
    for i in range(0,3):
        if board[i][0] == 0:
            allow_l = False
        elif board[i][2] == 0:
            allow_r = False


def UDrestrict():   #if empty space is on far bottom/top of board, it will restrict the up/down move
    global allow_u
    global allow_d
    allow_u = True
    allow_d = True
    for i in range(0,3):
        if board[0][i] == 0:
            allow_u = False
        if board[2][i] == 0 :
            allow_d = False


def find(board, num):   #returns the row and column of a number on the board        # 걍 empty space(0) 찾는거
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == num:
                return (i, j)  # row, col

# 0(empty space)을 "함수명" 방향으로 이동
def right():   #empty space switches positions with number directly left of it
    i, j = find(board, 0)
    board[i][j], board[i][j + 1] = board[i][j + 1], board[i][j]
    return board

def up():   #empty space switches positions with number directly below it
    i, j = find(board, 0)
    board[i][j], board[i-1][j] = board[i-1][j], board[i][j]
    return board

def left():   #empty space switches positions with number directly right of it
    i, j = find(board, 0)
    board[i][j], board[i][j - 1] = board[i][j - 1], board[i][j]
    return board

def down():   #empty space switches positions with number directly above it
    i, j = find(board, 0)
    board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]
    return board

class Node:   #creates a node with attributes: position, f_score            # position과 f_score를 속성으로 가지는 클래스, Node를 생성
    def __init__(self, position, f_score):
        self.position = position
        self.f_score = f_score  #allows storing more data into a single variable for ease


def in_closed(n1):   #makes sure a search node that was a previous search node is not queued
    '''
    - 집합, closed_set이 뭔지는 모르겠음 
        - 걍 set이라고 이름 붙인거임 
        - 집합 자료형 아님
    - 어쨌든 이거의 length가 1이면 in_closed 함수는 False를 반환함
    - n1 객체(node)가 closed_set에서 "start" key를 갖는 value(node)와 같다면 True 반환
        - closed_set 사전 자료형임?
    - 즉, closed_set 사전 자료형에 있는 node들 중 하나라면 True고...
    - 그런데 굳이 "start"를 해싱을 왜 해?
    - closed_set의 length가 1인지를 판단하는게 optimal moves에 중요하대
        - 왜
    - 어쨌든 in_closed 함수가 closedList에 해당 노드가 있는지를 확인하는 역할인거는 알았음
    - node가 empty space가 특정한 곳에 있는 (서로 다른) board라는 점이 처음에는 이해가 안 갔음
        - 지금은 감
    '''
    if len(closed_set) == 1:    #this is essential in saving a lot of time in finding the optimal moves
        return False
    if n1 == closed_set["start"]:
        return True
    if n1 in closed_set.values():
        return True
    return False

'''
- n1 object            
- 매개변수를 position으로 한 게 empyt space의 위치를 중점으로 하기 때문인 것 같음           
- board를 매개변수 name으로 하는게 더 직관적임
- opne_set은 우선순위 큐임
- nodes 사전은...
    - 모든 노드들을 저장함?
- 집합 자료구조도 {} ← 이거 씀
    - 주의하셈
- came_from은 이전 노드로부터 계층적으로 내려오는 노드들의 개수라는데
    - 트리 형태로 생각하면 child nodes들 모아놓은건가?
- closed_set dict의 start key에 해당하는 value로는 초기 board가 copy됨
    - closedList에 첫 번째로 들어가는게 초기 노드지
'''
n1 = Node(board, distance())  
open_set = PriorityQueue()  #priority queue
nodes = {}    #total nodes
closed_set = {}  #searched nodes
came_from = {}   #node number correlates to its previous node
closed_set["start"] = copy.deepcopy(board)   #inital board is a searched node

if is_solvable():       # 해당 board가 풀 수 있다면부터 시작            # 아니면 못 푼다고 print
    print("Finding solution... \n")
    while board != board_solved:   #loops until board is solved         # 될 때까지 loops
        RLrestrict()        # 상하좌우 제한
        UDrestrict()
        if allow_r:      #if able to move right
            n1.position = right()    #board moves right, and board state saved in n1 position attribute
            if in_closed(n1.position):  #checks if node was searched before
                left()    #if node searched previously, node will not be searched and so board goes back to previous state
            if not in_closed(n1.position):     #if node not searched
                nodes["node%s" % count] = n1.position  #node added to total nodes dictionary
                came_from["previous_node%s" % count] = copy.deepcopy(left())   #previous node added dictionary
                n1.position = copy.deepcopy(right())  #moves right again because previous caused board to move left
                h_score = distance()  #calculates h-score of search node
                n1.f_score = h_score + backtrack(n1.position)   #h-score + g-score = f-score
                open_set.put((n1.f_score, h_score, count, n1.position))  #values put in priority queue
                board = copy.deepcopy(board_previous)  #board is reverted 1 move back
                count += 1   #count is important in priority queue in event of a tie b/w f-score and h-score
        if allow_l:   #same procedure as being able to move right
            n1.position = left()
            if in_closed(n1.position):
                right()
            if not in_closed(n1.position):
                nodes["node%s" % count] = n1.position
                came_from["previous_node%s" % count] = copy.deepcopy(right())
                n1.position = copy.deepcopy(left())
                h_score = distance()
                n1.f_score = h_score + backtrack(n1.position)
                open_set.put((n1.f_score, h_score, count, n1.position))
                board = copy.deepcopy(board_previous)
                count += 1
        if allow_u:
            n1.position = up()
            if in_closed(n1.position):
                down()
            if not in_closed(n1.position):
                nodes["node%s" % count] = n1.position
                came_from["previous_node%s" % count] = copy.deepcopy(down())
                n1.position = copy.deepcopy(up())
                h_score = distance()
                n1.f_score = h_score + backtrack(n1.position)
                open_set.put((n1.f_score, h_score, count, n1.position))
                board = copy.deepcopy(board_previous)
                count += 1
        if allow_d:
            n1.position = down()
            if in_closed(n1.position):
                up()
            if not in_closed(n1.position):
                nodes["node%s" % count] = n1.position
                came_from["previous_node%s" % count] = copy.deepcopy(up())
                n1.position = copy.deepcopy(down())
                h_score = distance()
                n1.f_score = h_score + backtrack(n1.position)
                open_set.put((n1.f_score, h_score, count, n1.position))
                board = copy.deepcopy(board_previous)
                count += 1

            next_item = open_set.get()[3]   #next item equals the n1.position (board state)
            board = copy.deepcopy(next_item)   #board is made equal to the search node
            if board == board_solved:
                print("SOLVED")
                break
            closed_set["node%s" %count] = copy.deepcopy(next_item)  #search node is added to closed set
            board_previous = copy.deepcopy(board)  #previous node saved in board_previous

else:
    print("BOARD NOT SOLVABLE")

print(str(len(closed_set)) + " nodes explored")
print(str(len(nodes)) + " nodes total")