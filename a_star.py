class Node:
    def __init__(self, parent=None, position =None):
        # self는 인스턴스 자신
        # 생성한 인스턴스의 parent변수에 인자 parent를 저장
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return self.position == other.position # 인스턴스 자체가 아니라 인스턴스의 position 정보로 비교를 하도록 == 연산자를 재정의

def heuristic(node, goal, D=1, D2 =2 **0.5):    # Diagonal Distance
    dx = abs(node.position[0] - goal.position[0])
    dy = abs(node.position[1] - goal.position[1])
    return D * (dx + dy) + (D2 - 2 * D) * min(dx,dy)

def aStar(maze, start, end):
    # startNode와 endNode를 초기화
    startNode = Node(None, start)
    endNode = Node(None, end)

    # openList와 closedList 초기화
    openList = []
    closedList = []

    # openList에 시작 노드 추가
    openList.append(startNode)

    # endNode를 찾을 때까지 실행
    while openList:
        # 현재 노드 지정
        currentNode = openList[0]
        currentIdx = 0

        # 이미 같은 노드가 openList에 있을 때, openList에 있는 노드의 f가 더 크면
        # currentNode로 교체
        ## enumerate를 통해 openList를 인덱스와 아이템으로 이루어진 튜플을 만들어줌
        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                    currentNode = item
                    currentIdx = index
        
        # openList에서 제거하고 closedList에 추가
        openList.pop(currentIdx)
        closedList.append(currentNode)

        # 현재 노드가 목적지면 current.position 추가
        # current의 부모로 이동
        if currentNode == endNode:
                path = [] # 경로 반환
                current = currentNode
                while current is not None: # currentNode가 계속 있다면 반복
                    # x, y = current.position
                    # maze[x][y] = 7
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # 거꾸로 return
        
        children = []
        # 인접한 x, y좌표 전부?
        for newPosition in [(0,-1), (0,1), (-1,0), (1,0), (-1,-1), (-1,1), (1,-1), (1,1)]:
            # 노드 위치 업데이트?
            # 대각선 고려
            nodePosition = (
                currentNode.position[0] + newPosition[0],
                currentNode.position[1] + newPosition[1]
            ) # 튜플이구나
            # 미로 범위 안이어야 함
            within_range_criteria = [
                nodePosition[0] > (len(maze) - 1), nodePosition[0] < 0, nodePosition[1] > (len(maze[len(maze)-1]) - 1), nodePosition[1] < 0
            ]

            if any(within_range_criteria): # 하나라도 true면 범위 밖임
                continue
            if maze[nodePosition[0]][nodePosition[1]] != 0: # 1이면 장애물이 있는 것으로 간주
                continue
            
            new_node = Node(currentNode, nodePosition)
            children.append(new_node)

        for child in children:
                # 자식이 closedList에 있으면 continue
                if child in closedList:
                        continue
                
                child.g = currentNode.g + 1
                child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)

                child.f = child.g + child.h

                # 자식이 openList에 있고 g값이 더 크면 continue
                if len([openNode for openNode in openList if child == openNode and child.g > openNode.g]) > 0:
                    continue

                openList.append(child)

def main():
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    start = (0,0)
    end = (7,6)

    path = aStar(maze, start, end)
    print(path)

if __name__ == '__main__':
    main()



