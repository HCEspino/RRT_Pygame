import numpy as np

def distance(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

class Node():
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.children = set()
        self.cost = 0

    def computeCost(self, cost):
        if self.parent is not None:
            self.cost = self.parent.cost + cost
        else:
            self.cost = 0

class RRT():
    def __init__(self, maxWidth, maxHeight, start = None, goal = None):
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        if start is None:
            self.start = (maxWidth / 2, maxHeight / 2)
        else:
            self.start = start
        if goal is None:
            self.goal = (np.random.randint(0, maxWidth), np.random.randint(0, maxHeight))
        else:
            self.goal = goal

        self.nodes = set()

    def getPath(self):
        goalNode, _ = self.findClosest(self.goal)
        path = []
        while goalNode.parent is not None:
            path.append((goalNode.x, goalNode.y))
            goalNode = goalNode.parent

        path.reverse()
        return path

    def findClosest(self, pos):
        closest = None
        closestDist = float('inf')
        for node in self.nodes:
            dist = distance(pos, (node.x, node.y))
            if dist < closestDist:
                closest = node
                closestDist = dist
        return closest, closestDist
    
    def getMaxStep(self, pos1, pos2, maxstep = 10):
        if distance(pos1, pos2) < maxstep:
            return pos2
        else:
            return (pos1[0] + maxstep * (pos2[0] - pos1[0]) / distance(pos1, pos2), pos1[1] + maxstep * (pos2[1] - pos1[1]) / distance(pos1, pos2))

    def step(self, rewire=False):
        '''
        One step of RRT
        Returns pos of new node, position of node it's connected to, and True/False if finished
        '''
        if len(self.nodes) == 0:
            newnode = Node(self.start[0], self.start[1], None)
            newnode.computeCost(0)
            self.nodes.add(newnode)
            self.root = newnode
            return (newnode.x, newnode.y), None, False
        else:
            rand = (np.random.randint(0, self.maxWidth), np.random.randint(0, self.maxHeight))
            closest, dist = self.findClosest(rand)
            while dist < 20:
                rand = (np.random.randint(0, self.maxWidth), np.random.randint(0, self.maxHeight))
                closest, dist = self.findClosest(rand)

            pos = self.getMaxStep((closest.x, closest.y), rand, 25)

            newnode = Node(pos[0], pos[1], closest)
            newnode.computeCost(distance((closest.x, closest.y), (newnode.x, newnode.y)))
            self.nodes.add(newnode)

            closest.children.add(newnode)

            
            if rewire:

                mincost = newnode.cost
                mincostnode = closest

                #Check if node is wired good
                for node in self.nodes:
                    if node is not closest:
                        cost = distance((node.x, node.y), (newnode.x, newnode.y))
                        if cost < 50:
                            if node.cost + cost < mincost:
                                mincost = node.cost + cost
                                mincostnode = node

                closest.children.remove(newnode)
                newnode.parent = mincostnode

                mincostnode.children.add(newnode)
                newnode.computeCost(mincost)

                #Check if other nodes are better if wired to new one
                for node in self.nodes:
                    if node is not newnode.parent:
                        cost = distance((node.x, node.y), (newnode.x, newnode.y))
                        if cost < 20 and node.cost > newnode.cost + cost:
                            node.parent = newnode
                            newnode.children.add(node)
                            node.computeCost(cost)
                                

            if distance(pos, self.goal) < 20:
                return (newnode.x, newnode.y), (closest.x, closest.y), True
            else:
                return (newnode.x, newnode.y), (closest.x, closest.y), False
