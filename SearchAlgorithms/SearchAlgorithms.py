from queue import PriorityQueue
import numpy


class Node:
    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors.
    edgeCost = 0  # Represents the cost on the edge from any parent to this node.
    gOfN = 1000000000000000000  # Represents the total edge cost
    hOfN = None  # Represents the heuristic value
    vis = 0  # to show if it visited or not
    i = None
    j = None

    def __init__(self, value):
        self.value = value


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)
    nodes = []
    startNodeIndex = 0
    endID = -1
    maze = []

    def __init__(self, mazeStr, edgeCost=None):
        ''' mazeStr contains the full board
         The board is read row wise,
        the nodes are numbered 0-based starting
        the leftmost node'''
        self.edgeCost = edgeCost
        self.maze = []
        for i in mazeStr.split():
            self.maze.append(i.split(','))
        cols = len(mazeStr.split()[0].split(','))
        self.nodes.clear()
        for i in range(0, len(mazeStr), 2):
            x = Node(mazeStr[i])
            x.id = i // 2
            x.j = x.id % cols
            x.i = (x.id - x.j) // cols
            if x.id >= cols:
                x.up = self.nodes[i // 2 - cols]
                self.nodes[i // 2 - cols].down = x
            if x.id % 7 > 0:
                x.left = self.nodes[i // 2 - 1]
                self.nodes[i // 2 - 1].right = x
            if edgeCost is not None:
                x.edgeCost = edgeCost[x.id]
            if x.value == 'S':
                self.startNodeIndex = x.id
            if x.value == 'E':
                self.endID = x.id
            self.nodes.append(x)

    def reset_node(self):
        for i in self.nodes:
            i.vis = 0

    def DFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.fullPath = []
        v = [self.nodes[self.startNodeIndex]]
        self.nodes[self.startNodeIndex].vis = 1
        while len(v) > 0:
            x = v.pop()
            self.fullPath.append(x.id)
            y = x.right
            if y is not None:
                if y.value == 'E':
                    self.fullPath.append(y.id)
                    break
                elif y.vis == 0 and y.value != '#':
                    y.vis = 1
                    v.append(y)
            y = x.left
            if y is not None:
                if y.value == 'E':
                    self.fullPath.append(y.id)
                    break
                elif y.vis == 0 and y.value != '#':
                    y.vis = 1
                    v.append(y)
            y = x.down
            if y is not None:
                if y.value == 'E':
                    self.fullPath.append(y.id)
                    break
                elif y.vis == 0 and y.value != '#':
                    y.vis = 1
                    v.append(y)
            y = x.up
            if y is not None:
                if y.value == 'E':
                    self.fullPath.append(y.id)
                    break
                elif y.vis == 0 and y.value != '#':
                    y.vis = 1
                    v.append(y)
        return self.path, self.fullPath

    def BFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.fullPath = []
        self.reset_node()
        finish = -1
        stack = [self.startNodeIndex]
        i = 0
        while True:
            x = stack[i]
            i += 1
            right = self.nodes[x].right
            left = self.nodes[x].left
            up = self.nodes[x].up
            down = self.nodes[x].down
            if self.nodes[x].vis == 1:
                continue
            self.nodes[x].vis = 1
            self.fullPath.append(x)
            if self.nodes[x].value == 'E':
                finish = x
                break

            if up is not None and up.vis == 0 and up.value != '#':
                stack.append(up.id)
                up.previousNode = x

            if down is not None and down.vis == 0 and down.value != '#':
                stack.append(down.id)
                down.previousNode = x

            if left is not None and left.vis == 0 and left.value != '#':
                stack.append(left.id)
                left.previousNode = x

            if right is not None and right.vis == 0 and right.value != '#':
                stack.append(right.id)
                right.previousNode = x

        return self.path, self.fullPath

    def UCS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.fullPath = []
        self.reset_node()
        pq = PriorityQueue()
        pq._put((0, self.startNodeIndex))
        while pq.empty() == False:
            x = pq.get()
            right = self.nodes[x[1]].right
            left = self.nodes[x[1]].left
            up = self.nodes[x[1]].up
            down = self.nodes[x[1]].down
            if self.nodes[x[1]].vis == 1:
                continue
            self.fullPath.append(x[1])
            if self.nodes[x[1]].value == 'E':
                self.totalCost = x[0]
                break
            self.nodes[x[1]].vis = 1

            if up is not None and up.value != '#' and (up.gOfN > x[0] + up.edgeCost or up.gOfN is None):
                up.gOfN = x[0] + self.nodes[up.id].edgeCost
                pq.put_nowait((self.nodes[up.id].gOfN, up.id))
                up.previousNode = x[1]

            if down is not None and down.value != '#' and (down.gOfN > x[0] + down.edgeCost or down.gOfN is None):
                down.gOfN = x[0] + down.edgeCost
                pq.put_nowait((self.nodes[down.id].gOfN, down.id))
                down.previousNode = x[1]

            if left is not None and left.value != '#' and (left.gOfN > x[0] + left.edgeCost or left.gOfN is None):
                left.gOfN = x[0] + left.edgeCost
                pq.put_nowait((left.gOfN, left.id))
                left.previousNode = x[1]

            if right is not None and right.value != '#' and (right.gOfN > x[0] + right.edgeCost or right.gOfN is None):
                right.gOfN = x[0] + self.nodes[right.id].edgeCost
                pq.put_nowait((self.nodes[right.id].gOfN, right.id))
                right.previousNode = x[1]

        return self.path, self.fullPath, self.totalCost

    def Heuristic(self, flag):
        for i in self.nodes:
            if flag:
                i.hOfN = numpy.sqrt((i.i -self.nodes[self.endID].i) ** 2 + (i.j - self.nodes[self.endID].j) ** 2)
            else:
                i.hOfN = abs(i.i - self.nodes[self.endID].i) + abs(i.j - self.nodes[self.endID].j)

    def AStarEuclideanHeuristic(self):
        self.Heuristic(True)
        self.fullPath = []
        self.reset_node()
        self.nodes[self.startNodeIndex].gOfN = 0
        pq = [(self.nodes[self.startNodeIndex].hOfN, 0, self.startNodeIndex)]
        while len(pq):
            cur = min(pq)
            if self.nodes[cur[2]].value == 'E':
                self.totalCost = cur[1]
                self.fullPath.append(cur[2])
                break
            pq.remove(cur)
            if self.nodes[cur[2]].vis == 1:
                continue
            self.fullPath.append(cur[2])
            self.nodes[cur[2]].vis = 1
            up = self.nodes[cur[2]].up
            down = self.nodes[cur[2]].down
            left = self.nodes[cur[2]].left
            right = self.nodes[cur[2]].right
            if up is not None and self.nodes[up.id].vis == 0 and up.value != '#':
                g = up.edgeCost + cur[1]
                f = g + up.hOfN
                if up.gOfN > g:
                    up.gOfN = g
                    up.previousNode = cur[2]
                    pq.append((f, g, up.id))
            if down is not None and self.nodes[down.id].vis == 0 and down.value != '#':
                g = down.edgeCost + cur[1]
                f = g + down.hOfN
                if down.gOfN > g:
                    down.gOfN = g
                    down.previousNode = cur[2]
                    pq.append((f, g, down.id))
            if left is not None and self.nodes[left.id].vis == 0 and left.value != '#':
                g = left.edgeCost + cur[1]
                f = g + left.hOfN
                if left.gOfN > g:
                    left.gOfN = g
                    left.previousNode = cur[2]
                    pq.append((f, g, left.id))
            if right is not None and self.nodes[right.id].vis == 0 and right.value != '#':
                g = right.edgeCost + cur[1]
                f = g + right.hOfN
                if right.gOfN > g:
                    right.gOfN = g
                    right.previousNode = cur[2]
                    pq.append((f, g, right.id))
        return self.path, self.fullPath, self.totalCost

    def AStarManhattanHeuristic(self):
        self.Heuristic(False)
        self.fullPath = []
        self.reset_node()
        self.nodes[self.startNodeIndex].gOfN = 0
        pq = PriorityQueue()
        pq.put_nowait((self.nodes[self.startNodeIndex].hOfN, 0, self.startNodeIndex))
        while pq.empty() == False:
            cur = pq.get()
            if self.nodes[-cur[2]].value == 'E':
                self.totalCost = cur[1]
                self.fullPath.append(-cur[2])
                break
            if self.nodes[-cur[2]].vis == 1:
                continue
            self.fullPath.append(-cur[2])
            self.nodes[-cur[2]].vis = 1
            up = self.nodes[-cur[2]].up
            down = self.nodes[-cur[2]].down
            left = self.nodes[-cur[2]].left
            right = self.nodes[-cur[2]].right
            if up is not None and up.vis == 0 and up.value != '#':
                g = 1 + cur[1]
                f = g + up.hOfN
                if up.gOfN > g:
                    up.gOfN = g
                    up.previousNode = -cur[2]
                    pq.put_nowait((f, g, -up.id))
            if down is not None and down.vis == 0 and down.value != '#':
                g = 1 + cur[1]
                f = g + down.hOfN
                if down.gOfN > g:
                    down.gOfN = g
                    down.previousNode = -cur[2]
                    pq.put_nowait((f, g, -down.id))
            if left is not None and left.vis == 0 and left.value != '#':
                g = 1 + cur[1]
                f = g + left.hOfN
                if left.gOfN > g:
                    left.gOfN = g
                    left.previousNode = -cur[2]
                    pq.put_nowait((f, g, -left.id))
            if right is not None and right.vis == 0 and right.value != '#':
                g = 1 + cur[1]
                f = g + right.hOfN
                if right.gOfN > g:
                    right.gOfN = g
                    right.previousNode = -cur[2]
                    pq.put_nowait((f, g, -right.id))
        return self.path, self.fullPath, self.totalCost


def main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DFS()
    print('**DFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')

                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.BFS()
    print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
                                                                                                             , 100, 2, 15, 60, 100, 30, 2
                                                                                                             , 100, 2, 2, 2, 40, 30, 2, 2
                                                                                                             , 100, 100, 3, 15, 30, 100, 2
                                                                                                             , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.UCS()
    print('** UCS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
               #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
                                                                                                             , 100, 2, 15, 60, 100, 30, 2
                                                                                                             , 100, 2, 2, 2, 40, 30, 2, 2
                                                                                                             , 100, 100, 3, 15, 30, 100, 2
                                                                                                             , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.AStarEuclideanHeuristic()
    print('**ASTAR with Euclidean Heuristic **\nPath is: ' + str(path) + '\nFull Path is: ' + str(
        fullPath) + '\nTotal Cost: ' + str(TotalCost) + '\n\n')

            #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath, TotalCost = searchAlgo.AStarManhattanHeuristic()
    print('**ASTAR with Manhattan Heuristic **\nPath is: ' + str(path) + '\nFull Path is: ' + str(
        fullPath) + '\nTotal Cost: ' + str(TotalCost) + '\n\n')

main()

